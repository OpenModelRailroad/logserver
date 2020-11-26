from appsettings.models import Appsettings


class Helper:

    def is_simulator(self) -> bool:
        simulator = Appsettings.objects.get(key="simulator")
        if simulator == "checked":
            return True
        return False
