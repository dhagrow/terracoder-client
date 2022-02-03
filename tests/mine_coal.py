import terracoder

class Client(terracoder.Client):
    @property
    def drone(self):
        """Returns a drone specific client."""
        return Client(self._url, 'drone')

    @property
    def world(self):
        """Returns a world specific client."""
        return Client(self._url, 'world')

    def build_coal_mine(self):
        # start monitoring events
        events = self.events()

        # pick the first drone
        drone_id = self.drone.command('ids')[0]
        print('drone_id:', drone_id)

        # get the drone-control
        drone_control = self.world.command('get_type', type='drone-control')[0]

        # use the drone to run a scan for coal
        print('scanning ...')
        for tile in self.drone.command('scan', drone_id=drone_id):
            if 'coal' in tile['resources']:
                break
        else:
            raise Exception('no resources found')

        while True:
            # travel to the coal
            dst = tile['position']
            print(f'travelling to {dst} ...')
            self.drone.command('travel', drone_id=drone_id, position=dst)
            self.wait_for_event(events, 'drone-task-idle')

            # mine the coal
            print('mining ...')
            self.drone.command('mine', drone_id=drone_id, resource='coal')
            self.wait_for_event(events, 'drone-task-idle')

            # take the 🎶coal to control🎶
            print('travelling to control ...')
            self.drone.command('travel', drone_id=drone_id,
                position=drone_control['position'])
            self.wait_for_event(events, 'drone-task-idle')

            # unload the coal
            print('unloading ...')
            self.drone.command('transfer', drone_id=drone_id,
                system_id=drone_control['id'],
                resource='coal')

def main():
    Client().build_coal_mine()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
