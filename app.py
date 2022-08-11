"""
***Door control with WebApp integration***
GitHub: https://github.com/Trogiken/chicken-door
"""


def main():
    from source.base_logger import log
    log.info("App Startup...")

    from source.door import Door
    from source.auto import Auto
    import source.disk as disk
    import anvil.server
    import os

    save = disk.Save()
    log.info("Save object created")
    config = disk.Config()
    log.info("Config object created")

    loaded_save = save.load()
    log.info("Save Loaded")
    log.debug(f"Loaded Save Data: {loaded_save}")

    loaded_config = config.load()
    io = loaded_config['gpio']
    prop = loaded_config['properties']
    log.info("Config Loaded")
    log.debug(f"Loaded Config Data: {loaded_config}")

    door = Door(relay1=io['relay1'], relay2=io['relay2'],
                sw1=io['switch1'], sw2=io['switch2'], sw3=io['switch3'], max_travel=prop['max_travel'])
    log.info("Door object created")

    sunrise_offset = loaded_save['sunrise_offset']
    sunset_offset = loaded_save['sunset_offset']
    auto = Auto(door=door, zone=str(prop['timezone']),
                latitude=float(prop['latitude']), longitude=float(prop['longitude']),
                sunrise_offset=int(sunrise_offset), sunset_offset=int(sunset_offset))
    log.info("Automation object created")

    try:
        anvil_id = prop['anvil_id']
        log.debug(f"Connection ID: {anvil_id}")
        anvil.server.connect(anvil_id)
        log.info("Server Connection Made")

        if loaded_save['automation']:
            auto.run()
        if loaded_save['auxiliary']:
            door.run_aux()

        @anvil.server.callable
        def run_auto():
            """Calls auto.run()"""
            log.debug("CALLED")
            auto.run()

        @anvil.server.callable
        def stop_auto():
            """Calls auto.stop()"""
            log.debug("CALLED")
            auto.stop()

        @anvil.server.callable
        def run_aux():
            """Calls door.run_aux()"""
            log.debug("CALLED")
            door.run_aux()

        @anvil.server.callable
        def stop_aux():
            """Calls door.stop_aux()"""
            log.debug("CALLED")
            door.stop_aux()

        @anvil.server.callable
        def change_rise(offset):
            """Changes auto object variable (sunrise_offset) to (offset) and saves the new value"""
            log.debug("CALLED")
            auto.sunrise_offset = offset
            save.change('sunrise_offset', offset)

        @anvil.server.callable
        def change_set(offset):
            """Changes auto object variable (sunset_offset) to (offset) and saves the new value"""
            log.debug("CALLED")
            auto.sunset_offset = offset
            save.change('sunset_offset', offset)

        @anvil.server.callable
        def times():
            """Returns sunrise and sunset times in a dictionary"""
            log.debug("CALLED")
            return {'sunrise': auto.active_sunrise(),
                    'sunset': auto.active_sunset()}

        @anvil.server.callable
        def c_state(variable=None):
            """
            Read save file

                Parameters:
                    variable (str), optional: key in dictionary

                Returns:
                    save.load() (dict): all data
                    save.load()[variable] (str, int, float, bool): value of specified key
            """
            log.debug("CALLED")
            if variable is not None:
                return save.load()[variable]
            else:
                return save.load()

        @anvil.server.callable
        def rpi_status():
            """Called by WebApp to check if it still has connection to this program, Returns None"""
            return

        @anvil.server.callable
        def door_status():
            """Returns func call door.get_status()"""
            return door.get_status()

        @anvil.server.callable
        def reset_config():
            """"Calls save.reset()"""
            save.reset()
            return

        @anvil.server.callable
        def shutdown(parm='h'):
            """
            Shutdown or Restart system

            If parm is changed to 'r' the system will restart

                Parameters:
                    parm (str), optional: Shutdown flag
            """
            if parm == 'h':
                log.warning("Shutting Down...")
            elif parm == 'r':
                log.warning("Restarting...")
            else:
                return
            anvil.server.disconnect()
            stop_aux()
            stop_auto()
            door.cleanup()
            os.system(f'sudo shutdown -{parm} now')

        @anvil.server.callable
        def move(opt):
            """Takes opt (1 or 2) and calls door.move(opt)"""
            log.debug("CALLED")
            door.move(opt)

        @anvil.server.callable
        def change(variable, value):
            """Calls save.change(variable, value)"""
            log.debug("CALLED")
            save.change(variable, value)

        log.info("Startup Complete!")
        anvil.server.wait_forever()
    except Exception:
        log.exception("EXCEPTION")
        anvil.server.disconnect()
        return


if __name__ == '__main__':
    main()
