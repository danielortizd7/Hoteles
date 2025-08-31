# Generated manually for renaming name to nombre

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0003_alter_roomtype_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='roomtype',
            old_name='name',
            new_name='nombre',
        ),
    ]
