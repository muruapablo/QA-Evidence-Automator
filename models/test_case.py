"""
Modelos de datos para Test Cases de Azure DevOps
"""
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class TestStep:
    """Representa un paso de prueba en Azure DevOps"""
    index: int
    action: str
    expected_result: str

    @classmethod
    def from_azure_format(cls, step_data: Dict[str, Any], index: int) -> "TestStep":
        """
        Crea un TestStep desde el formato de Azure DevOps

        Args:
            step_data: Diccionario con datos del paso desde Azure
            index: Índice del paso (1, 2, 3, ...)

        Returns:
            Instancia de TestStep
        """
        return cls(
            index=index,
            action=step_data.get("action", "").strip(),
            expected_result=step_data.get("expectedResult", "").strip()
        )

    def to_formatted_string(self) -> str:
        """Convierte el paso a texto formateado para documento"""
        return f"Paso {self.index}:\nAcción: {self.action}\nResultado Esperado: {self.expected_result}"


@dataclass
class TestCase:
    """Representa un Test Case de Azure DevOps"""
    id: int
    title: str
    description: str = ""
    steps: List[TestStep] = field(default_factory=list)
    state: str = "Design"
    priority: int = 2
    assigned_to: Optional[str] = None
    area_path: Optional[str] = None
    iteration_path: Optional[str] = None
    tags: List[str] = field(default_factory=list)

    # Metadatos adicionales
    created_date: Optional[datetime] = None
    modified_date: Optional[datetime] = None
    created_by: Optional[str] = None

    @classmethod
    def from_azure_response(cls, work_item: Dict[str, Any]) -> "TestCase":
        """
        Crea un TestCase desde la respuesta de Azure DevOps API

        Args:
            work_item: Diccionario con datos del work item desde Azure

        Returns:
            Instancia de TestCase

        Ejemplo de estructura de Azure DevOps:
        {
            "id": 123,
            "fields": {
                "System.Title": "Login con credenciales válidas",
                "System.Description": "<div>Verificar login...</div>",
                "System.State": "Design",
                "Microsoft.VSTS.Common.Priority": 2,
                "System.AssignedTo": "user@example.com",
                "System.AreaPath": "Project\\QA",
                "System.IterationPath": "Project\\Sprint 1",
                "System.Tags": "smoke; regression",
                "Microsoft.VSTS.TCM.Steps": "<steps>...</steps>"
            }
        }
        """
        fields = work_item.get("fields", {})

        # Extraer pasos de prueba
        steps = cls._parse_test_steps(fields.get("Microsoft.VSTS.TCM.Steps", ""))

        # Extraer tags
        tags_str = fields.get("System.Tags", "")
        tags = [tag.strip() for tag in tags_str.split(";")] if tags_str else []

        # Parsear fechas
        created_date = cls._parse_date(fields.get("System.CreatedDate"))
        modified_date = cls._parse_date(fields.get("System.ChangedDate"))

        return cls(
            id=work_item.get("id"),
            title=fields.get("System.Title", "Sin título"),
            description=cls._clean_html(fields.get("System.Description", "")),
            steps=steps,
            state=fields.get("System.State", "Design"),
            priority=fields.get("Microsoft.VSTS.Common.Priority", 2),
            assigned_to=fields.get("System.AssignedTo", {}).get("displayName") if isinstance(fields.get("System.AssignedTo"), dict) else None,
            area_path=fields.get("System.AreaPath"),
            iteration_path=fields.get("System.IterationPath"),
            tags=tags,
            created_date=created_date,
            modified_date=modified_date,
            created_by=fields.get("System.CreatedBy", {}).get("displayName") if isinstance(fields.get("System.CreatedBy"), dict) else None
        )

    @staticmethod
    def _parse_test_steps(steps_xml: str) -> List[TestStep]:
        """
        Parsea los pasos de prueba desde el formato XML de Azure DevOps

        Formato esperado:
        <steps id="0" last="2">
            <step id="2" type="ActionStep">
                <parameterizedString isformatted="true">
                    &lt;DIV&gt;&lt;P&gt;Ingresar usuario y contraseña&lt;/P&gt;&lt;/DIV&gt;
                </parameterizedString>
                <parameterizedString isformatted="true">
                    &lt;DIV&gt;&lt;P&gt;Login exitoso&lt;/P&gt;&lt;/DIV&gt;
                </parameterizedString>
                <description/>
            </step>
        </steps>
        """
        import re
        from html import unescape

        steps = []

        if not steps_xml:
            return steps

        # Extraer todos los steps usando regex
        step_pattern = r'<step[^>]*type="ActionStep"[^>]*>(.*?)</step>'
        step_matches = re.findall(step_pattern, steps_xml, re.DOTALL)

        for idx, step_content in enumerate(step_matches, start=1):
            # Extraer action y expected result
            params = re.findall(r'<parameterizedString[^>]*>(.*?)</parameterizedString>', step_content, re.DOTALL)

            if len(params) >= 2:
                action = TestCase._clean_html(unescape(params[0]))
                expected_result = TestCase._clean_html(unescape(params[1]))

                steps.append(TestStep(
                    index=idx,
                    action=action,
                    expected_result=expected_result
                ))

        return steps

    @staticmethod
    def _clean_html(html_content: str) -> str:
        """Limpia contenido HTML para obtener texto plano"""
        import re
        from html import unescape

        if not html_content:
            return ""

        # Decodificar entidades HTML
        text = unescape(html_content)

        # Remover tags HTML
        text = re.sub(r'<[^>]+>', '', text)

        # Limpiar espacios múltiples
        text = re.sub(r'\s+', ' ', text)

        return text.strip()

    @staticmethod
    def _parse_date(date_str: Optional[str]) -> Optional[datetime]:
        """Parsea fecha desde formato ISO de Azure DevOps"""
        if not date_str:
            return None

        try:
            # Azure DevOps usa formato ISO 8601
            return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        except (ValueError, AttributeError):
            return None

    def get_all_steps_formatted(self) -> str:
        """Retorna todos los pasos formateados como texto"""
        if not self.steps:
            return "Sin pasos definidos"

        return "\n\n".join([step.to_formatted_string() for step in self.steps])

    def to_context_dict(self) -> Dict[str, str]:
        """
        Convierte el TestCase a un diccionario compatible con el contexto actual
        de la aplicación (testId, step, description)

        Returns:
            Dict con formato: {"testId": str, "step": str, "description": str}
        """
        return {
            "testId": f"TC{self.id}_{self._sanitize_title(self.title)}",
            "step": "Caso_Completo",
            "description": self._build_full_description()
        }

    def _sanitize_title(self, title: str) -> str:
        """Sanitiza el título para usarlo como ID"""
        import re
        # Remover caracteres especiales y espacios
        sanitized = re.sub(r'[^\w\s-]', '', title)
        sanitized = re.sub(r'[-\s]+', '_', sanitized)
        return sanitized[:50]  # Limitar longitud

    def _build_full_description(self) -> str:
        """Construye descripción completa con todos los detalles del caso"""
        parts = []

        # Título y descripción
        parts.append(f"<h2>{self.title}</h2>")

        if self.description:
            parts.append(f"<p><strong>Descripción:</strong> {self.description}</p>")

        # Metadata
        metadata = []
        if self.priority:
            metadata.append(f"Prioridad: {self.priority}")
        if self.state:
            metadata.append(f"Estado: {self.state}")
        if self.assigned_to:
            metadata.append(f"Asignado a: {self.assigned_to}")

        if metadata:
            parts.append(f"<p><em>{' | '.join(metadata)}</em></p>")

        # Pasos de prueba
        if self.steps:
            parts.append("<h3>Pasos de Prueba:</h3>")
            parts.append("<ol>")
            for step in self.steps:
                parts.append(f"<li><strong>Acción:</strong> {step.action}<br><strong>Resultado Esperado:</strong> {step.expected_result}</li>")
            parts.append("</ol>")

        return "\n".join(parts)


@dataclass
class TestSuite:
    """Representa un Test Suite de Azure DevOps"""
    id: int
    name: str
    plan_id: int
    test_case_count: int = 0

    @classmethod
    def from_azure_response(cls, suite_data: Dict[str, Any]) -> "TestSuite":
        """Crea TestSuite desde respuesta de Azure DevOps"""
        return cls(
            id=suite_data.get("id"),
            name=suite_data.get("name", "Sin nombre"),
            plan_id=suite_data.get("plan", {}).get("id") if suite_data.get("plan") else 0,
            test_case_count=suite_data.get("testCaseCount", 0)
        )


@dataclass
class TestPlan:
    """Representa un Test Plan de Azure DevOps"""
    id: int
    name: str
    state: str = "Active"
    description: str = ""
    area_path: Optional[str] = None
    iteration_path: Optional[str] = None

    @classmethod
    def from_azure_response(cls, plan_data: Dict[str, Any]) -> "TestPlan":
        """Crea TestPlan desde respuesta de Azure DevOps"""
        return cls(
            id=plan_data.get("id"),
            name=plan_data.get("name", "Sin nombre"),
            state=plan_data.get("state", "Active"),
            description=plan_data.get("description", ""),
            area_path=plan_data.get("areaPath"),
            iteration_path=plan_data.get("iteration")
        )
