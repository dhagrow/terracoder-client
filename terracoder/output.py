def world_state(res):
    def gen():
        data = res.json()
        yield f'tick: {data["tick"]}'

        for sys in data['systems']:
            width = max(len(k) for k in sys)
            sys_id = sys.pop('id')
            yield f'{"id":->{width}}: {sys_id}'
            for k, v in sys.items():
                yield f'{k:>{width}}: {v}'

    return '\n'.join(gen())

def drone_get(res):
    def gen():
        data = res.json()
        width = max(len(k) for k in data)
        for k, v in data.items():
            yield f'{k:>{width}}: {v}'
    return '\n'.join(gen())

def drone_state(res):
    def gen():
        data = res.json()
        for drone in data:
            width = max(len(k) for k in drone)
            drone_id = drone.pop('id')
            yield f'{"id":->{width}}: {drone_id}'
            for k, v in drone.items():
                yield f'{k:>{width}}: {v}'

    return '\n'.join(gen())
