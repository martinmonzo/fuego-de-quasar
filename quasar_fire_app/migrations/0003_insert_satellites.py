from django.db import migrations
from quasar_fire_app.models.satellite import Satellite


class Migration(migrations.Migration):

    initial = False

    dependencies = [
        ('quasar_fire_app', '0002_auto_20210306_0450',),
    ]

    def insertData(apps, schema_editor):
        Satellite = apps.get_model('quasar_fire_app', 'Satellite')
        kenobi = Satellite(name='kenobi', x_position=-500.0,y_position=-200.0)
        kenobi.save()
        skywalker = Satellite(name='skywalker', x_position=100.0,y_position=-100.0)
        skywalker.save()
        sato = Satellite(name='sato', x_position=500.0,y_position=100.0)
        sato.save()

    operations = [
        migrations.RunPython(insertData),
    ]
