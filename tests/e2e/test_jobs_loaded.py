import os
import json
from django.core.urlresolvers import reverse
from webtest import TestApp
from thclient import TreeherderJobCollection
from datadiff import diff

from treeherder.webapp.wsgi import application
from tests import test_utils


def test_pending_job_available(jm, initial_data, pending_jobs_stored):
    webapp = TestApp(application)
    resp = webapp.get(
        reverse('jobs-list', kwargs={'project': jm.project})
    )
    jobs = resp.json

    assert len(jobs) ==1

    assert jobs[0]['state'] == 'pending'


def test_running_job_available(jm, initial_data, running_jobs_stored):
    webapp = TestApp(application)
    resp = webapp.get(
        reverse('jobs-list', kwargs={'project': jm.project})
    )
    jobs = resp.json

    assert len(jobs) ==1

    assert jobs[0]['state'] == 'running'


def test_completed_job_available(jm, initial_data, completed_jobs_loaded):
    webapp = TestApp(application)
    resp = webapp.get(
        reverse('jobs-list', kwargs={'project': jm.project})
    )
    jobs = resp.json

    assert len(jobs) == 1
    assert jobs[0]['state'] == 'completed'


def test_pending_stored_to_running_loaded(jm, initial_data, pending_jobs_stored, running_jobs_stored):
    '''
    tests a job transition from pending to running
    given a pending job loaded in the objects store
    if I store and load the same job with status running,
    the latter is shown in the jobs endpoint
    '''
    webapp = TestApp(application)
    resp = webapp.get(
        reverse('jobs-list', kwargs={'project': jm.project})
    )
    jobs = resp.json

    assert len(jobs) == 1
    assert jobs[0]['state'] == 'running'


def test_finished_job_to_running(jm, initial_data, completed_jobs_loaded, running_jobs_stored):
    '''
    tests that a job finished cannot change state
    '''
    webapp = TestApp(application)
    resp = webapp.get(
        reverse('jobs-list', kwargs={'project': jm.project})
    )
    jobs = resp.json

    assert len(jobs) == 1
    assert jobs[0]['state'] == 'completed'


def test_running_job_to_pending(jm, initial_data, running_jobs_stored, pending_jobs_stored):
    '''
    tests that a job transition from pending to running
    cannot happen
    '''
    webapp = TestApp(application)
    resp = webapp.get(
        reverse('jobs-list', kwargs={'project': jm.project})
    )
    jobs = resp.json

    assert len(jobs) == 1
    assert jobs[0]['state'] == 'running'


def test_objectstore_wih_artifacts_keeps_artifacts(
        jm, initial_data, test_base_dir, result_set_stored, mock_log_parser):
    '''
    tests that a job object with artifacts submitted to the objectstore endpoint
    is propertly stored
    '''
    source_file = os.path.join(test_base_dir, 'sample_data',
                               'job_with_artifact.json')
    job_object = json.loads(open(source_file).read())[0]
    job_object['revision_hash'] = result_set_stored[0]['revision_hash']

    tjc = TreeherderJobCollection()
    tj = tjc.get_job(job_object)
    tjc.add(tj)

    test_utils.post_collection(jm.project, tjc)
    jm.process_objects(1, raise_errors=True)

    actual_artifacts = jm.get_job_artifact_list(0, 1)[0]

    del actual_artifacts['id']
    del actual_artifacts['job_id']

    expected_artifact = job_object['job']['artifacts'][0]

    assert expected_artifact == actual_artifacts, diff(
        expected_artifact, actual_artifacts
    )
