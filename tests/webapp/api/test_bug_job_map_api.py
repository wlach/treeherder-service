import datetime
import json
import random
from time import time

import pytest
from django.core.urlresolvers import reverse
from rest_framework.test import APIClient

from treeherder.model.models import (BugJobMap,
                                     Job)


@pytest.mark.parametrize('test_no_auth,test_duplicate_handling', [
    (True, False),
    (False, False),
    (False, True)])
def test_create_bug_job_map(eleven_jobs_stored, mock_message_broker, jm,
                            test_user, test_no_auth, test_duplicate_handling):
    """
    test creating a single note via endpoint
    """

    client = APIClient()
    if not test_no_auth:
        client.force_authenticate(user=test_user)

    job = jm.get_job_list(0, 1)[0]

    submit_obj = {
        u"job_id": job["id"],
        u"bug_id": 1L,
        u"type": u"manual"
    }

    # if testing duplicate handling, submit twice
    if test_duplicate_handling:
        num_times = 2
    else:
        num_times = 1

    for i in range(num_times):
        resp = client.post(
            reverse("bug-job-map-list", kwargs={"project": jm.project}),
            submit_obj, expect_errors=test_no_auth)

    if test_no_auth:
        assert resp.status_code == 403
        assert BugJobMap.objects.count() == 0
    else:
        assert BugJobMap.objects.count() == 1
        bug_job_map = BugJobMap.objects.all()

        assert bug_job_map.job.project_specific_id == submit_obj['job_id']
        assert bug_job_map.bug_id == 1L
        assert bug_job_map.type == submit_obj['type']
        assert bug_job_map.who.email == test_user.email


def test_bug_job_map_list(webapp, jm, eleven_jobs_stored, test_user):
    """
    test retrieving a list of bug_job_map
    """
    jobs = Job.objects.all()[:10]
    bugs = [random.randint(0, 100) for i in range(0, len(jobs))]
    submit_timestamp = datetime.datetime.now()

    expected = list()

    for (i, job) in enumerate(jobs):
        BugJobMap.objects.create(job=job, bug_id=bugs[i],
                                 type=BugJobMap.MANUAL,
                                 submit_timestamp=submit_timestamp,
                                 who=test_user)
        expected.append({
            "job_id": job.project_specific_id,
            "bug_id": bugs[i],
            "type": "manual",
            "submit_timestamp": int(time.mktime(submit_timestamp.timetuple())),
            "who": test_user.email
        })
        submit_timestamp += datetime.timedelta(seconds=1)

    resp = webapp.get(
        reverse("bug-job-map-list", kwargs={"project": jm.project}))

    # The order of the bug-job-map list is not guaranteed.
    assert sorted(resp.json) == sorted(expected)


def test_bug_job_map_detail(webapp, eleven_jobs_stored, test_repository,
                            test_user):
    """
    test retrieving a list of bug_job_map
    """
    job = Job.objects.all()[0]
    bug_id = random.randint(0, 100)

    expected = list()

    submit_timestamp = datetime.datetime.now()
    BugJobMap.objects.create(job=job,
                             bug_id=bug_id,
                             type=BugJobMap.MANUAL,
                             submit_timestamp=submit_timestamp,
                             who=test_user)

    pk = "{0}-{1}".format(job.project_specific_id, bug_id)

    resp = webapp.get(
        reverse("bug-job-map-detail", kwargs={
            "project": test_repository.name,
            "pk": pk
        })
    )

    expected = {
        "job_id": job.project_specific_id,
        "bug_id": bug_id,
        "type": "manual",
        "submit_timestamp": int(time.mktime(submit_timestamp.timetuple())),
        "who": test_user.email
    }

    assert resp.json == expected


@pytest.mark.parametrize('test_no_auth', [True, False])
def test_bug_job_map_delete(webapp, eleven_jobs_stored, test_repository,
                            test_user, test_no_auth):
    """
    test deleting a bug_job_map object
    """
    job = Job.objects.all()[0]
    bug_id = random.randint(0, 100)

    submit_timestamp = datetime.datetime.now()
    BugJobMap.objects.create(job=job,
                             bug_id=bug_id,
                             type=BugJobMap.MANUAL,
                             submit_timestamp=submit_timestamp,
                             who=test_user)

    client = APIClient()
    if not test_no_auth:
        client.force_authenticate(user=test_user)

    pk = "{0}-{1}".format(job.project_specific_id, bug_id)

    resp = client.delete(
        reverse("bug-job-map-detail", kwargs={
            "project": test_repository.name,
            "pk": pk
        })
    )

    if test_no_auth:
        assert resp.status_code == 403
        assert BugJobMap.objects.count() == 1
    else:
        content = json.loads(resp.content)
        assert content == {"message": "Bug job map deleted"}
        assert BugJobMap.objects.count() == 0
