# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Log'
        db.delete_table(u'stats_log')


    def backwards(self, orm):
        # Adding model 'Log'
        db.create_table(u'stats_log', (
            ('url', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('referer', self.gf('django.db.models.fields.CharField')(default='-', max_length=256)),
            ('useragent', self.gf('django.db.models.fields.CharField')(default='-', max_length=256)),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
            ('ip', self.gf('django.db.models.fields.CharField')(default='-', max_length=256)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('method', self.gf('django.db.models.fields.CharField')(default='-', max_length=256)),
        ))
        db.send_create_signal(u'stats', ['Log'])


    models = {
        
    }

    complete_apps = ['stats']