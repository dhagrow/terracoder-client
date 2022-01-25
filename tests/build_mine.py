import coder

class Client(coder.Client):
    def build_coal_mine(self):
        events = self.events()
        # start generator
        next(events)

        bot_id = self.command('bot/ids')[0]

        # scan
        for tile in self.command('bot/scan', bot_id=bot_id):
            if 'coal' in tile['resources']:
                break
        else:
            raise Exception('no resources found')

        # travel
        dst = tile['position']
        self.command('bot/travel', bot_id=bot_id, destination=dst)
        self.wait_for_idle(events)

        # build
        self.command('bot/build', bot_id=bot_id, structure='coal-mine')
        self.wait_for_idle(events)

    def wait_for_idle(self, events):
        for event in events:
            print('event:', event)
            if event['name'] == 'bot-task-idle':
                break

def main():
    Client().build_coal_mine()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
