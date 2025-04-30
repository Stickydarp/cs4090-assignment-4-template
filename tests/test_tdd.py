import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.tasks import sort_tasks_by_priority, sort_tasks_by_due_date,sort_tasks_by_difficulty


def test_sort_tasks_by_priority():
    # Given a list of tasks with different priorities
    tasks = [
        {"id": 1, "title": "Task 1", "priority": "Low"},
        {"id": 2, "title": "Task 2", "priority": "High"},
        {"id": 3, "title": "Task 3", "priority": "Medium"}
    ]
    
    # When sorting the tasks by priority
    sorted_tasks = sort_tasks_by_priority(tasks, ["Low", "Medium", "High"])
    
    # Then the tasks should be sorted in the order of Low, Medium, High
    assert sorted_tasks[0]["id"] == 1, "First task should be Task 1 (Low priority)"
    assert sorted_tasks[1]["id"] == 3, "Second task should be Task 3 (Medium priority)"
    assert sorted_tasks[2]["id"] == 2, "Third task should be Task 2 (High priority)"

    resorted_tasks = sort_tasks_by_priority(tasks, ["High", "Medium", "Low"])
    assert resorted_tasks[0]["id"] == 2, "First task should be Task 2 (High priority)"
    assert resorted_tasks[1]["id"] == 3, "Second task should be Task 3 (Medium priority)"   
    assert resorted_tasks[2]["id"] == 1, "Third task should be Task 1 (Low priority)"


def test_sort_tasks_by_due_date():
    # Given a list of tasks with different due dates
    tasks = [
        {"id": 1, "title": "Task 1", "due_date": "2023-10-05"},
        {"id": 2, "title": "Task 2", "due_date": "2023-10-01"},
        {"id": 3, "title": "Task 3", "due_date": "2023-10-03"}
    ]
    order = "Ascending"  # Ascending order
    # When sorting the tasks by due date
    sorted_tasks = sort_tasks_by_due_date(tasks, order)
    
    # Then the tasks should be sorted in ascending order of due date
    assert sorted_tasks[0]["id"] == 2, "First task should be Task 2 (earliest due date)"
    assert sorted_tasks[1]["id"] == 3, "Second task should be Task 3 (next due date)"
    assert sorted_tasks[2]["id"] == 1, "Third task should be Task 1 (latest due date)"

    order = "desc"  # Descending order
    resorted_tasks = sort_tasks_by_due_date(tasks, order)
    # Then the tasks should be sorted in descending order of due date
    assert resorted_tasks[0]["id"] == 1, "First task should be Task 1 (latest due date)"
    assert sorted_tasks[1]["id"] == 3, "Second task should be Task 3 (next due date)"
    assert sorted_tasks[0]["id"] == 2, "last task should be Task 2 (earliest due date)"

def test_sort_tasks_by_difficulty():
    # Given a list of tasks with different difficulties
    tasks = [
        {"id": 1, "title": "Task 1", "difficulty": "Easy"},
        {"id": 2, "title": "Task 2", "difficulty": "Hard"},
        {"id": 3, "title": "Task 3", "difficulty": "Medium"}
    ]
    
    # When sorting the tasks by difficulty
    sorted_tasks = sort_tasks_by_difficulty(tasks, ["Easy", "Medium", "Hard"])
    assert sorted_tasks[0]["id"] == 1, "First task should be Task 1 (Easy difficulty)"
    assert sorted_tasks[1]["id"] == 3, "Second task should be Task 3 (Medium difficulty)"
    assert sorted_tasks[2]["id"] == 2, "Third task should be Task 2 (Hard difficulty)"
