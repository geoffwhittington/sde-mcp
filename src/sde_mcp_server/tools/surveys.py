"""Survey-related tools"""
import json
from typing import List, Optional

from fastmcp import Context

from ..server import mcp, api_client, init_api_client
from ._base import build_params


@mcp.tool()
async def get_project_survey(ctx: Context, project_id: int) -> str:
    """Get the complete survey structure for a project (all available questions and ALL possible answers). Use this to see what survey questions exist and what answers are available. Use get_survey_answers_for_project to see only the answers that are currently selected for a project."""
    global api_client
    if api_client is None:
        api_client = init_api_client()
    result = api_client.get_project_survey(project_id)
    return json.dumps(result, indent=2)


@mcp.tool()
async def update_project_survey(ctx: Context, project_id: int, answers: List[str], survey_complete: Optional[bool] = None) -> str:
    """Update project survey with answer IDs"""
    global api_client
    if api_client is None:
        api_client = init_api_client()
    data = {"answers": answers}
    if survey_complete is not None:
        data["survey_complete"] = survey_complete
    result = api_client.update_project_survey(project_id, data)
    return json.dumps(result, indent=2)


@mcp.tool()
async def find_survey_answers(ctx: Context, project_id: int, search_texts: List[str]) -> str:
    """Find survey answers by text"""
    global api_client
    if api_client is None:
        api_client = init_api_client()
    result = api_client.find_survey_answers_by_text(project_id, search_texts)
    return json.dumps(result, indent=2)


@mcp.tool()
async def set_project_survey_by_text(ctx: Context, project_id: int, answer_texts: List[str], survey_complete: Optional[bool] = None) -> str:
    """Set/REPLACE all project survey answers by text. This REPLACES all existing answers with the new ones. Use ONLY when user wants to completely replace all answers. Use add_survey_answers_by_text if user says 'add' or wants to keep existing answers."""
    global api_client
    if api_client is None:
        api_client = init_api_client()
    
    search_results = api_client.find_survey_answers_by_text(project_id, answer_texts)
    answer_ids = []
    not_found = []
    for text, info in search_results.items():
        if info.get('id'):
            answer_ids.append(info['id'])
        else:
            not_found.append(text)
    
    if not_found:
        result = {
            "error": f"Could not find answers for: {', '.join(not_found)}",
            "search_results": search_results
        }
    else:
        data = {"answers": answer_ids}
        if survey_complete is not None:
            data["survey_complete"] = survey_complete
        update_result = api_client.update_project_survey(project_id, data)
        result = {
            "success": True,
            "matched_answers": search_results,
            "answer_ids_used": answer_ids,
            "update_result": update_result
        }
    return json.dumps(result, indent=2)


@mcp.tool()
async def remove_survey_answers_by_text(ctx: Context, project_id: int, answer_texts_to_remove: List[str]) -> str:
    """Remove survey answers by text"""
    global api_client
    if api_client is None:
        api_client = init_api_client()
    
    current_survey = api_client.get_project_survey(project_id)
    current_answer_ids = current_survey.get('answers', [])
    search_results = api_client.find_survey_answers_by_text(project_id, answer_texts_to_remove)
    
    ids_to_remove = []
    not_found = []
    for text, info in search_results.items():
        if info.get('id'):
            ids_to_remove.append(info['id'])
        else:
            not_found.append(text)
    
    new_answer_ids = [aid for aid in current_answer_ids if aid not in ids_to_remove]
    data = {"answers": new_answer_ids}
    update_result = api_client.update_project_survey(project_id, data)
    
    result = {
        "success": True,
        "removed_answers": {text: info for text, info in search_results.items() if info.get('id')},
        "ids_removed": ids_to_remove,
        "not_found": not_found,
        "remaining_answer_count": len(new_answer_ids),
        "update_result": update_result
    }
    return json.dumps(result, indent=2)


@mcp.tool()
async def add_survey_answers_by_text(ctx: Context, project_id: int, answer_texts_to_add: List[str]) -> str:
    """ADD survey answers by text to existing answers. Use when user says 'add', 'include', or wants to add to existing answers. This ADDS new answers while preserving all existing ones. Use set_project_survey_by_text ONLY if user explicitly wants to REPLACE all answers."""
    global api_client
    if api_client is None:
        api_client = init_api_client()
    result = api_client.add_survey_answers_by_text(project_id, answer_texts_to_add, fuzzy_threshold=0.75, auto_resolve_dependencies=True)
    return json.dumps(result, indent=2)


@mcp.tool()
async def get_survey_answers_for_project(ctx: Context, project_id: int, format: str = "summary") -> str:
    """Get the survey answers FOR A PROJECT that are currently selected/assigned. Use when user asks 'show me the survey answers for project X', 'what answers are set for project', 'survey answers for project', or 'current answers for project'. Returns only the answers that are currently selected for the project, not all available answers. Use get_project_survey to see the full survey structure with all available questions and answers."""
    global api_client
    if api_client is None:
        api_client = init_api_client()
    
    survey = api_client.get_project_survey(project_id)
    current_answer_ids = survey.get('answers', [])
    
    if not current_answer_ids:
        result = {"project_id": project_id, "message": "No answers are currently assigned to this survey", "answer_count": 0}
    else:
        answer_details = {}
        for section in survey.get('sections', []):
            section_title = section.get('title', 'Untitled Section')
            for question in section.get('questions', []):
                question_text = question.get('text', 'Untitled Question')
                for answer in question.get('answers', []):
                    answer_id = answer.get('id')
                    if answer_id in current_answer_ids:
                        answer_details[answer_id] = {
                            'text': answer.get('text', 'N/A'),
                            'question': question_text,
                            'section': section_title,
                            'question_id': question.get('id')
                        }
        
        if format == "summary":
            result = {
                "project_id": project_id,
                "answer_count": len(current_answer_ids),
                "answers": [details['text'] for details in answer_details.values()],
                "answer_ids": current_answer_ids
            }
        elif format == "detailed":
            result = {
                "project_id": project_id,
                "answer_count": len(current_answer_ids),
                "answers": [{"text": details['text'], "question": details['question'], "answer_id": aid} for aid, details in answer_details.items()]
            }
        elif format == "grouped":
            grouped = {}
            for aid, details in answer_details.items():
                section = details['section']
                if section not in grouped:
                    grouped[section] = []
                grouped[section].append({"question": details['question'], "answer": details['text']})
            result = {"project_id": project_id, "answer_count": len(current_answer_ids), "sections": grouped}
        else:
            result = {"error": f"Unknown format: {format}"}
    return json.dumps(result, indent=2)


@mcp.tool()
async def commit_survey_draft(ctx: Context, project_id: int) -> str:
    """Commit the survey draft to publish the survey and generate countermeasures"""
    global api_client
    if api_client is None:
        api_client = init_api_client()
    result = api_client.commit_survey_draft(project_id)
    return json.dumps(result, indent=2)

