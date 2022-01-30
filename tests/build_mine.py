import terracoder

class Client(terracoder.Client):
    @property
    def drone(self):
        """Returns a drone specific client."""
        return Client(self._url, 'drone')

    def build_coal_mine(self):
        # start monitoring events
        events = self.events()

        # pick the first drone
        drone_id = self.drone.command('ids')[0]

        # use the drone to run a scan for coal
        for tile in self.command('drone/scan', drone_id=drone_id):
            if 'coal' in tile['resources']:
                break
        else:
            raise Exception('no resources found')

        # travel to the coal
        dst = tile['position']
        self.command('drone/travel', drone_id=drone_id, destination=dst)
        self.wait_for_event(events, 'drone-task-idle')

        # build a mine to mine the coal
        self.command('drone/build', drone_id=drone_id, type='coal-mine')
        self.wait_for_event(events, 'drone-task-idle')

def main():
    Client().build_coal_mine()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
