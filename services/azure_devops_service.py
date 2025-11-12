"""
Servicio para interactuar con Azure DevOps API
Gestiona la comunicación con los endpoints de Test Plans, Test Suites y Test Cases
"""
import os
import base64
import logging
from typing import List, Optional, Dict, Any
import requests
from requests.exceptions import RequestException, Timeout

from models.test_case import TestCase, TestSuite, TestPlan


# Configurar logging
logger = logging.getLogger(__name__)


class AzureDevOpsError(Exception):
    """Excepción personalizada para errores de Azure DevOps"""
    pass


class AzureDevOpsService:
    """Cliente para interactuar con Azure DevOps REST API"""

    def __init__(
        self,
        organization: str,
        project: str,
        personal_access_token: str,
        api_version: str = "7.1"
    ):
        """
        Inicializa el cliente de Azure DevOps

        Args:
            organization: Nombre de la organización en Azure DevOps
            project: Nombre del proyecto
            personal_access_token: Personal Access Token (PAT) para autenticación
            api_version: Versión de la API (por defecto 7.1)

        Raises:
            ValueError: Si faltan parámetros requeridos
        """
        if not all([organization, project, personal_access_token]):
            raise ValueError("Organization, project y personal_access_token son requeridos")

        self.organization = organization
        self.project = project
        self.api_version = api_version

        # Base URLs
        self.base_url = f"https://dev.azure.com/{organization}/{project}"
        self.base_api_url = f"{self.base_url}/_apis"

        # Configurar autenticación
        self.headers = self._create_auth_headers(personal_access_token)

        # Timeout por defecto (en segundos)
        self.timeout = 30

        logger.info(f"AzureDevOpsService inicializado para {organization}/{project}")

    @staticmethod
    def _create_auth_headers(pat: str) -> Dict[str, str]:
        """
        Crea los headers de autenticación para Azure DevOps

        Azure DevOps usa Basic Auth con:
        - Usuario: (vacío)
        - Contraseña: PAT

        Args:
            pat: Personal Access Token

        Returns:
            Dict con headers de autenticación
        """
        # Codificar en base64: :{PAT}
        credentials = f":{pat}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()

        return {
            "Authorization": f"Basic {encoded_credentials}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Realiza una petición HTTP a Azure DevOps API

        Args:
            method: Método HTTP (GET, POST, etc.)
            endpoint: Endpoint relativo (ej: "testplan/plans")
            params: Parámetros de query string
            json_data: Datos JSON para el body (POST/PUT)

        Returns:
            Respuesta JSON como diccionario

        Raises:
            AzureDevOpsError: Si hay error en la petición
        """
        # Construir URL completa
        url = f"{self.base_api_url}/{endpoint}"

        # Agregar api-version a params
        if params is None:
            params = {}
        params["api-version"] = self.api_version

        try:
            logger.debug(f"Request: {method} {url} params={params}")

            response = requests.request(
                method=method,
                url=url,
                headers=self.headers,
                params=params,
                json=json_data,
                timeout=self.timeout
            )

            # Verificar código de estado
            response.raise_for_status()

            # Retornar JSON
            return response.json()

        except Timeout:
            error_msg = f"Timeout al conectar con Azure DevOps: {url}"
            logger.error(error_msg)
            raise AzureDevOpsError(error_msg)

        except RequestException as e:
            error_msg = f"Error en petición a Azure DevOps: {str(e)}"
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_details = e.response.json()
                    error_msg += f" - Detalles: {error_details}"
                except:
                    error_msg += f" - Status: {e.response.status_code}"

            logger.error(error_msg)
            raise AzureDevOpsError(error_msg)

    # ============================================
    # TEST PLANS
    # ============================================

    def get_test_plans(self) -> List[TestPlan]:
        """
        Obtiene todos los Test Plans del proyecto

        Returns:
            Lista de TestPlan

        API Endpoint:
            GET https://dev.azure.com/{organization}/{project}/_apis/testplan/plans?api-version=7.1
        """
        try:
            response = self._make_request("GET", "testplan/plans")

            plans = []
            for plan_data in response.get("value", []):
                try:
                    plan = TestPlan.from_azure_response(plan_data)
                    plans.append(plan)
                except Exception as e:
                    logger.warning(f"Error parseando test plan {plan_data.get('id')}: {e}")
                    continue

            logger.info(f"Se obtuvieron {len(plans)} test plans")
            return plans

        except AzureDevOpsError:
            raise
        except Exception as e:
            raise AzureDevOpsError(f"Error obteniendo test plans: {str(e)}")

    def get_test_plan(self, plan_id: int) -> Optional[TestPlan]:
        """
        Obtiene un Test Plan específico por ID

        Args:
            plan_id: ID del test plan

        Returns:
            TestPlan o None si no existe

        API Endpoint:
            GET https://dev.azure.com/{organization}/{project}/_apis/testplan/plans/{planId}?api-version=7.1
        """
        try:
            response = self._make_request("GET", f"testplan/plans/{plan_id}")
            return TestPlan.from_azure_response(response)

        except AzureDevOpsError as e:
            if "404" in str(e):
                logger.warning(f"Test plan {plan_id} no encontrado")
                return None
            raise

    # ============================================
    # TEST SUITES
    # ============================================

    def get_test_suites(self, plan_id: int) -> List[TestSuite]:
        """
        Obtiene todos los Test Suites de un Test Plan

        Args:
            plan_id: ID del test plan

        Returns:
            Lista de TestSuite

        API Endpoint:
            GET https://dev.azure.com/{organization}/{project}/_apis/testplan/Plans/{planId}/suites?api-version=7.1
        """
        try:
            response = self._make_request("GET", f"testplan/Plans/{plan_id}/suites")

            suites = []
            for suite_data in response.get("value", []):
                try:
                    suite = TestSuite.from_azure_response(suite_data)
                    suites.append(suite)
                except Exception as e:
                    logger.warning(f"Error parseando test suite {suite_data.get('id')}: {e}")
                    continue

            logger.info(f"Se obtuvieron {len(suites)} test suites del plan {plan_id}")
            return suites

        except AzureDevOpsError:
            raise
        except Exception as e:
            raise AzureDevOpsError(f"Error obteniendo test suites del plan {plan_id}: {str(e)}")

    def get_test_suite(self, plan_id: int, suite_id: int) -> Optional[TestSuite]:
        """
        Obtiene un Test Suite específico

        Args:
            plan_id: ID del test plan
            suite_id: ID del test suite

        Returns:
            TestSuite o None si no existe

        API Endpoint:
            GET https://dev.azure.com/{organization}/{project}/_apis/testplan/Plans/{planId}/suites/{suiteId}?api-version=7.1
        """
        try:
            response = self._make_request("GET", f"testplan/Plans/{plan_id}/suites/{suite_id}")
            return TestSuite.from_azure_response(response)

        except AzureDevOpsError as e:
            if "404" in str(e):
                logger.warning(f"Test suite {suite_id} del plan {plan_id} no encontrado")
                return None
            raise

    # ============================================
    # TEST CASES
    # ============================================

    def get_test_cases_from_suite(self, plan_id: int, suite_id: int) -> List[TestCase]:
        """
        Obtiene todos los Test Cases de un Test Suite

        Args:
            plan_id: ID del test plan
            suite_id: ID del test suite

        Returns:
            Lista de TestCase (con información básica, sin pasos)

        API Endpoint:
            GET https://dev.azure.com/{organization}/{project}/_apis/testplan/Plans/{planId}/Suites/{suiteId}/TestCase?api-version=7.1
        """
        try:
            response = self._make_request(
                "GET",
                f"testplan/Plans/{plan_id}/Suites/{suite_id}/TestCase"
            )

            test_cases = []
            for tc_data in response.get("value", []):
                try:
                    # Obtener detalles completos del test case (con pasos)
                    tc_id = tc_data.get("testCase", {}).get("id")
                    if tc_id:
                        full_test_case = self.get_test_case(tc_id)
                        if full_test_case:
                            test_cases.append(full_test_case)
                except Exception as e:
                    logger.warning(f"Error obteniendo test case: {e}")
                    continue

            logger.info(f"Se obtuvieron {len(test_cases)} test cases del suite {suite_id}")
            return test_cases

        except AzureDevOpsError:
            raise
        except Exception as e:
            raise AzureDevOpsError(f"Error obteniendo test cases del suite {suite_id}: {str(e)}")

    def get_test_case(self, test_case_id: int) -> Optional[TestCase]:
        """
        Obtiene un Test Case completo por ID (incluyendo pasos)

        Args:
            test_case_id: ID del test case (work item ID)

        Returns:
            TestCase con todos los detalles o None si no existe

        API Endpoint:
            GET https://dev.azure.com/{organization}/{project}/_apis/wit/workitems/{id}?api-version=7.1
        """
        try:
            response = self._make_request("GET", f"wit/workitems/{test_case_id}")
            return TestCase.from_azure_response(response)

        except AzureDevOpsError as e:
            if "404" in str(e):
                logger.warning(f"Test case {test_case_id} no encontrado")
                return None
            raise

    # ============================================
    # UTILIDADES
    # ============================================

    def test_connection(self) -> bool:
        """
        Prueba la conexión con Azure DevOps

        Returns:
            True si la conexión es exitosa, False en caso contrario
        """
        try:
            # Intentar obtener información del proyecto
            self._make_request("GET", "projects")
            logger.info("Conexión con Azure DevOps exitosa")
            return True

        except AzureDevOpsError as e:
            logger.error(f"Error al probar conexión: {e}")
            return False

    @classmethod
    def from_env(cls) -> Optional["AzureDevOpsService"]:
        """
        Crea instancia de AzureDevOpsService desde variables de entorno

        Variables requeridas:
            - AZURE_DEVOPS_ORG
            - AZURE_DEVOPS_PROJECT
            - AZURE_DEVOPS_PAT

        Variables opcionales:
            - AZURE_DEVOPS_API_VERSION (default: 7.1)

        Returns:
            Instancia de AzureDevOpsService o None si falta configuración
        """
        org = os.getenv("AZURE_DEVOPS_ORG")
        project = os.getenv("AZURE_DEVOPS_PROJECT")
        pat = os.getenv("AZURE_DEVOPS_PAT")
        api_version = os.getenv("AZURE_DEVOPS_API_VERSION", "7.1")

        if not all([org, project, pat]):
            logger.warning("Faltan variables de entorno para Azure DevOps")
            return None

        return cls(
            organization=org,
            project=project,
            personal_access_token=pat,
            api_version=api_version
        )


# Singleton global (opcional, para facilitar acceso)
_azure_service: Optional[AzureDevOpsService] = None


def get_azure_service() -> Optional[AzureDevOpsService]:
    """
    Obtiene la instancia singleton del servicio de Azure DevOps

    Returns:
        Instancia de AzureDevOpsService o None si no está configurado
    """
    global _azure_service

    if _azure_service is None:
        _azure_service = AzureDevOpsService.from_env()

    return _azure_service


def is_azure_devops_enabled() -> bool:
    """
    Verifica si la integración con Azure DevOps está habilitada

    Returns:
        True si está habilitada y configurada, False en caso contrario
    """
    enabled = os.getenv("AZURE_DEVOPS_ENABLED", "false").lower() == "true"

    if not enabled:
        return False

    # Verificar que esté configurado
    service = get_azure_service()
    return service is not None
