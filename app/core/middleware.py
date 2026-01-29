import logging
import os

logger = logging.getLogger(__name__)


class DomainRoutingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 접속한 도메인 확인 (포트 번호 제외)
        host = request.get_host().split(":")[0]

        # 환경 변수에서 별도 도메인 가져오기 (기본값: 로컬 테스트용)
        target_domain = os.environ.get("SECONDARY_DOMAIN", "agency.local")

        # 해당 도메인으로 메인 페이지('/') 접속 시
        if target_domain in host and request.path == "/":
            logger.info(
                f"Domain routing: Redirecting {host}/ to /korea-culture-arts-translation-agency"
            )
            # 내부적으로 URL 경로를 변경 (리다이렉트 아님)
            request.path_info = "/korea-culture-arts-translation-agency"

        response = self.get_response(request)
        return response
