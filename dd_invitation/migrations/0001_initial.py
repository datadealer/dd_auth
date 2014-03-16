# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Token'
        db.create_table('dd_invitation_token', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('value', self.gf('django.db.models.fields.CharField')(default='2d7ddbf0a3dd0c2d250fe78f3ef217e5', unique=True, max_length=255)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('consumed', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('dd_invitation', ['Token'])


    def backwards(self, orm):
        # Deleting model 'Token'
        db.delete_table('dd_invitation_token')


    models = {
        'dd_invitation.token': {
            'Meta': {'object_name': 'Token'},
            'consumed': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'default': "'810810f720b499ca60e44b692f853aa5'", 'unique': 'True', 'max_length': '255'})
        }
    }

    complete_apps = ['dd_invitation']