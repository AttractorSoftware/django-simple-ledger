# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Transaction'
        db.create_table(u'ledger_transaction', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('agent_from_content_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='agent_from_type', to=orm['contenttypes.ContentType'])),
            ('agent_from_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('agent_to_content_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='agent_to_type', to=orm['contenttypes.ContentType'])),
            ('agent_to_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('amount', self.gf('django.db.models.fields.DecimalField')(max_digits=15, decimal_places=2)),
            ('transaction_type', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('batch_id', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('transaction', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='reasoning_transaction', null=True, to=orm['ledger.Transaction'])),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'ledger', ['Transaction'])


    def backwards(self, orm):
        # Deleting model 'Transaction'
        db.delete_table(u'ledger_transaction')


    models = {
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'ledger.transaction': {
            'Meta': {'object_name': 'Transaction'},
            'agent_from_content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'agent_from_type'", 'to': u"orm['contenttypes.ContentType']"}),
            'agent_from_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'agent_to_content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'agent_to_type'", 'to': u"orm['contenttypes.ContentType']"}),
            'agent_to_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '15', 'decimal_places': '2'}),
            'batch_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'transaction': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'reasoning_transaction'", 'null': 'True', 'to': u"orm['ledger.Transaction']"}),
            'transaction_type': ('django.db.models.fields.CharField', [], {'max_length': '2'})
        }
    }

    complete_apps = ['ledger']