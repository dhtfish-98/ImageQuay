"""Preserve executable source metadata in the wheel staging tree."""
from pathlib import Path as DeliveryPath
from shutil import copymode as delivery_copy_mode
from setuptools.command.build_py import build_py as DeliveryBuildBase
class DeliveryBuild(DeliveryBuildBase):
    def run(delivery_self):
        super().run()
        delivery_source=DeliveryPath(__file__).resolve().parent
        for delivery_file in delivery_source.rglob('*'):
            if delivery_file.is_file():
                delivery_output=DeliveryPath(delivery_self.build_lib)/delivery_file.relative_to(delivery_source)
                if delivery_output.is_file():delivery_copy_mode(delivery_file,delivery_output)
