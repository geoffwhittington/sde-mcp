"""
SD Elements API Client

A Python client for interacting with the SD Elements API v2.
"""

import os
import requests
from typing import Dict, Any, Optional, List, Union
from urllib.parse import urljoin, urlparse
import json


class SDElementsAPIError(Exception):
    """Base exception for SD Elements API errors"""
    pass


class SDElementsAuthError(SDElementsAPIError):
    """Authentication error"""
    pass


class SDElementsNotFoundError(SDElementsAPIError):
    """Resource not found error"""
    pass


class SDElementsAPIClient:
    """
    SD Elements API v2 Client
    
    Provides methods to interact with SD Elements API endpoints.
    """
    
    def __init__(self, host: str, api_key: str):
        """
        Initialize the SD Elements API client.
        
        Args:
            host: SD Elements host URL (e.g., "https://your-instance.sdelements.com")
            api_key: API key for authentication
        """
        self.host = host.rstrip('/')
        self.api_key = api_key
        self.base_url = f"{self.host}/api/v2/"
        
        # Default headers
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Token {self.api_key}',
            'Accept': 'application/json'
        }
        
        # Session for connection pooling
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def _make_request(
        self, 
        method: str, 
        endpoint: str, 
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Make an HTTP request to the SD Elements API.
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint (relative to base_url)
            params: URL parameters
            data: Form data
            json_data: JSON data for request body
            
        Returns:
            Response data as dictionary
            
        Raises:
            SDElementsAPIError: For API errors
            SDElementsAuthError: For authentication errors
            SDElementsNotFoundError: For 404 errors
        """
        url = urljoin(self.base_url, endpoint.lstrip('/'))
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                params=params,
                data=data,
                json=json_data,
                timeout=30
            )
            
            # Handle different status codes
            if response.status_code == 401:
                raise SDElementsAuthError("Authentication failed. Check your API key.")
            elif response.status_code == 403:
                raise SDElementsAuthError("Access forbidden. Check your permissions.")
            elif response.status_code == 404:
                raise SDElementsNotFoundError(f"Resource not found: {url}")
            elif response.status_code >= 400:
                try:
                    error_data = response.json()
                    error_msg = error_data.get('detail', f"API error: {response.status_code}")
                except:
                    error_msg = f"HTTP {response.status_code}: {response.text}"
                raise SDElementsAPIError(error_msg)
            
            # Try to parse JSON response
            try:
                return response.json()
            except json.JSONDecodeError:
                if response.status_code == 204:  # No content
                    return {}
                return {"text": response.text}
                
        except requests.exceptions.ConnectionError:
            raise SDElementsAPIError(f"Connection error: Unable to connect to {self.host}")
        except requests.exceptions.Timeout:
            raise SDElementsAPIError("Request timeout")
        except requests.exceptions.RequestException as e:
            raise SDElementsAPIError(f"Request error: {str(e)}")
    
    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a GET request"""
        return self._make_request('GET', endpoint, params=params)
    
    def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a POST request"""
        return self._make_request('POST', endpoint, json_data=data)
    
    def put(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a PUT request"""
        return self._make_request('PUT', endpoint, json_data=data)
    
    def patch(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a PATCH request"""
        return self._make_request('PATCH', endpoint, json_data=data)
    
    def delete(self, endpoint: str) -> Dict[str, Any]:
        """Make a DELETE request"""
        return self._make_request('DELETE', endpoint)
    
    # Projects API
    def list_projects(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """List all projects"""
        return self.get('projects/', params)
    
    def get_project(self, project_id: int, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Get project by ID"""
        return self.get(f'projects/{project_id}/', params)
    
    def create_project(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new project"""
        return self.post('projects/', data)
    
    def update_project(self, project_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update a project"""
        return self.patch(f'projects/{project_id}/', data)
    
    def delete_project(self, project_id: int) -> Dict[str, Any]:
        """Delete a project"""
        return self.delete(f'projects/{project_id}/')
    
    # Applications API
    def list_applications(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """List all applications"""
        return self.get('applications/', params)
    
    def get_application(self, app_id: int, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Get application by ID"""
        return self.get(f'applications/{app_id}/', params)
    
    def create_application(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new application"""
        return self.post('applications/', data)
    
    def update_application(self, app_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an application"""
        return self.patch(f'applications/{app_id}/', data)
    
    # Countermeasures API
    def list_countermeasures(self, project_id: int, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """List countermeasures for a project"""
        if params is None:
            params = {}
        params['project'] = project_id
        return self.get('countermeasures/', params)
    
    def get_countermeasure(self, countermeasure_id: int, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Get countermeasure by ID"""
        return self.get(f'countermeasures/{countermeasure_id}/', params)
    
    def update_countermeasure(self, countermeasure_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update a countermeasure"""
        return self.patch(f'countermeasures/{countermeasure_id}/', data)
    
    # Users API
    def list_users(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """List all users"""
        return self.get('users/', params)
    
    def get_user(self, user_id: int, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Get user by ID"""
        return self.get(f'users/{user_id}/', params)
    
    def get_current_user(self) -> Dict[str, Any]:
        """Get current authenticated user"""
        return self.get('users/me/')
    
    # Business Units API
    def list_business_units(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """List all business units"""
        return self.get('business-units/', params)
    
    def get_business_unit(self, bu_id: int, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Get business unit by ID"""
        return self.get(f'business-units/{bu_id}/', params)
    
    # Groups API
    def list_groups(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """List all groups"""
        return self.get('groups/', params)
    
    def get_group(self, group_id: int, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Get group by ID"""
        return self.get(f'groups/{group_id}/', params)
    
    # Generic API request method
    def api_request(
        self, 
        method: str, 
        endpoint: str, 
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Make a custom API request to any endpoint.
        
        Args:
            method: HTTP method (GET, POST, PUT, PATCH, DELETE)
            endpoint: API endpoint
            params: URL parameters
            data: Request body data
            
        Returns:
            API response data
        """
        if method.upper() in ['GET', 'DELETE']:
            return self._make_request(method.upper(), endpoint, params=params)
        else:
            return self._make_request(method.upper(), endpoint, params=params, json_data=data)
    
    def test_connection(self) -> bool:
        """
        Test the API connection and authentication.
        
        Returns:
            True if connection and authentication are successful
        """
        try:
            self.get_current_user()
            return True
        except (SDElementsAPIError, SDElementsAuthError):
            return False 