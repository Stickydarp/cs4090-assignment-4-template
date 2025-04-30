import pytest
import sys
import os
import json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.tasks import load_tasks, save_tasks, generate_unique_id, filter_tasks_by_priority,filter_tasks_by_category,filter_tasks_by_completion, search_tasks,get_overdue_tasks

##using pytest parameterize
@pytest.mark.parametrize("file_path, expected_type, expected_non_empty", [
    ("test.json", list, True)
])
def test_load_tasks(file_path, expected_type, expected_non_empty):
    tasks = load_tasks(file_path)
    assert isinstance(tasks, expected_type), f"load_tasks should return a {expected_type.__name__}"
    assert (len(tasks) > 0) == expected_non_empty, "load_tasks should return a non-empty list of tasks"
    assert isinstance(tasks[0], dict), "each task should be a dictionary"

def test_load_tasks_empty():
    tasks = load_tasks("tests/empty.json")
    assert isinstance(tasks, list), "load_tasks should return a list even if the file is empty"
    assert len(tasks) == 0, "load_tasks should return an empty list when the file is empty"\

def test_load_tasks_corrupted_json(tmp_path):
    # Create a corrupted JSON file
    corrupted_file = tmp_path / "corrupted.json"
    corrupted_file.write_text("{invalid_json}")  # Invalid JSON content

    # Test the load_tasks function
    tasks = load_tasks(corrupted_file)
    
    # Verify the behavior
    assert tasks == [], "load_tasks should return an empty list for corrupted JSON files"

def test_generate_unique_id():
    tasks = [{"id": 1}, {"id": 2}, {"id": 3}]
    new_id = generate_unique_id(tasks)
    assert new_id == 4, "generate_unique_id should return the next available ID"

def test_filter_tasks_by_priority():
    tasks = [
        {"id": 1, "priority": "High"},
        {"id": 2, "priority": "Medium"},
        {"id": 3, "priority": "Low"}
    ]
    high_priority_tasks = filter_tasks_by_priority(tasks, "High")
    assert len(high_priority_tasks) == 1, "filter_tasks_by_priority should return tasks with High priority"
    assert high_priority_tasks[0]["id"] == 1, "The task with High priority should have ID 1"

def test_filter_tasks_by_catagory():
    tasks = [
        {"id": 1, "category": "Work"},
        {"id": 2, "category": "Personal"},
        {"id": 3, "category": "Work"}
    ]
    work_tasks = filter_tasks_by_category(tasks, "Work")
    assert len(work_tasks) == 2, "filter_tasks_by_category should return tasks in the Work category"
    assert all(task["category"] == "Work" for task in work_tasks), "All returned tasks should be in the Work category"






##-------------------------bdd tests-____________________________----------------------------------------------------------------

def test_filter_tasks_by_completion_returns_only_completed_tasks():
    # Given a list of tasks with some completed and some not completed
    tasks = [
        {"id": 1, "completed": True},
        {"id": 2, "completed": False},
        {"id": 3, "completed": True}
    ]

    # When filter_tasks_by_completion is called with the argument to filter completed tasks
    completed_tasks = filter_tasks_by_completion(tasks, True)

    # Then it should return only the tasks that are marked as completed
    assert len(completed_tasks) == 2, "Expected filter_tasks_by_completion to return two completed tasks"
    assert all(task["completed"] for task in completed_tasks), "Expected all returned tasks to be marked as completed"

def test_save_tasks_creates_file_with_correct_data(tmp_path):
    # Given a list of tasks and a file path
    tasks = [{"id": 1, "title": "Test Task"}]
    file_path = tmp_path / "test.json"

    # When save_tasks is called
    save_tasks(tasks, file_path)

    # Then the file should be created and contain the correct data
    assert file_path.exists(), "Expected save_tasks to create a file at the specified path"
    with open(file_path, "r") as f:
        saved_tasks = json.load(f)
    assert saved_tasks == tasks, "Expected the saved tasks to match the input tasks"


def test_search_tasks_returns_matching_tasks():
    # Given a list of tasks
    tasks = [
        {"id": 1, "title": "Test Task", "description": "This is a test task"},
        {"id": 2, "title": "Another Task", "description": "This is another task"},
        {"id": 3, "title": "Sample Task", "description": "This is a sample task"}
    ]

    # When search_tasks is called with a query
    search_results = search_tasks(tasks, "test")

    # Then it should return tasks that match the query
    assert len(search_results) == 1, "Expected search_tasks to return one matching task"
    assert search_results[0]["id"] == 1, "Expected the matching task to have ID 1"


def test_get_overdue_tasks_returns_only_overdue_tasks():
    from datetime import datetime, timedelta

    # Given a list of tasks with due dates
    tasks = [
        {"id": 1, "due_date": (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")},  # Overdue
        {"id": 2, "due_date": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")},  # Not overdue
        {"id": 3, "due_date": (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d")}   # Overdue
    ]

    # When get_overdue_tasks is called
    overdue_tasks = get_overdue_tasks(tasks)

    # Then it should return only the overdue tasks
    assert len(overdue_tasks) == 2, "Expected get_overdue_tasks to return two overdue tasks"
    assert all(datetime.strptime(task["due_date"], "%Y-%m-%d") < datetime.now() for task in overdue_tasks), \
        "Expected all returned tasks to be overdue"


def test_get_overdue_tasks_returns_empty_list_when_no_tasks():
    # Given an empty list of tasks
    tasks = []

    # When get_overdue_tasks is called
    overdue_tasks = get_overdue_tasks(tasks)

    # Then it should return an empty list
    assert len(overdue_tasks) == 0, "Expected get_overdue_tasks to return an empty list when there are no tasks"

