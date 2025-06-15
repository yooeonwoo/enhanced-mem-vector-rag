#!/bin/bash

# Enhanced Memory-Vector RAG - Coolify 배포 스크립트
# 사용법: ./deploy-to-coolify.sh

set -e  # 에러 발생 시 스크립트 종료

echo "🚀 Enhanced Memory-Vector RAG Coolify 배포 시작..."

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 함수 정의
print_step() {
    echo -e "${BLUE}📋 $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# 1. 환경 확인
print_step "환경 확인 중..."

# 필수 파일 존재 확인
if [[ ! -f "docker-compose.coolify.yml" ]]; then
    print_error "docker-compose.coolify.yml 파일이 없습니다!"
    exit 1
fi

if [[ ! -f ".env" ]]; then
    print_error ".env 파일이 없습니다!"
    exit 1
fi

print_success "필수 파일 확인 완료"

# 2. Docker Compose 설정 검증
print_step "Docker Compose 설정 검증 중..."

if command -v docker-compose &> /dev/null; then
    docker-compose -f docker-compose.coolify.yml config > /dev/null
    print_success "Docker Compose 설정 유효"
else
    print_warning "docker-compose 명령어를 찾을 수 없습니다. 설정 검증을 건너뛰겠습니다."
fi

# 3. 환경 변수 확인
print_step "환경 변수 확인 중..."

# 필수 환경 변수 목록
required_vars=(
    "OPENAI_API_KEY"
    "QDRANT_URL"
    "QDRANT_API_KEY"
    "NEO4J_URI"
    "NEO4J_USERNAME"
    "NEO4J_PASSWORD"
    "SUPABASE_URL"
    "SUPABASE_KEY"
)

# .env 파일 로드 (검증용)
if [[ -f ".env" ]]; then
    source .env
fi

missing_vars=()
for var in "${required_vars[@]}"; do
    if [[ -z "${!var}" ]]; then
        missing_vars+=("$var")
    fi
done

if [[ ${#missing_vars[@]} -gt 0 ]]; then
    print_error "다음 환경 변수들이 설정되지 않았습니다:"
    for var in "${missing_vars[@]}"; do
        echo "  - $var"
    done
    echo ""
    echo "💡 .env 파일을 확인하고 누락된 변수들을 설정해주세요."
    exit 1
fi

print_success "필수 환경 변수 확인 완료"

# 4. 네트워크 연결 테스트
print_step "외부 서비스 연결 테스트 중..."

# OpenAI API 테스트
if command -v curl &> /dev/null; then
    if curl -s --max-time 10 -H "Authorization: Bearer $OPENAI_API_KEY" \
       "https://api.openai.com/v1/models" > /dev/null; then
        print_success "OpenAI API 연결 성공"
    else
        print_warning "OpenAI API 연결 실패 - API 키를 확인해주세요"
    fi

    # Qdrant 연결 테스트
    if curl -s --max-time 10 -H "api-key: $QDRANT_API_KEY" \
       "$QDRANT_URL/collections" > /dev/null; then
        print_success "Qdrant 연결 성공"
    else
        print_warning "Qdrant 연결 실패 - URL과 API 키를 확인해주세요"
    fi

    # Supabase 연결 테스트
    if curl -s --max-time 10 -H "apikey: $SUPABASE_KEY" \
       "$SUPABASE_URL/rest/v1/" > /dev/null; then
        print_success "Supabase 연결 성공"
    else
        print_warning "Supabase 연결 실패 - URL과 키를 확인해주세요"
    fi
else
    print_warning "curl 명령어를 찾을 수 없습니다. 연결 테스트를 건너뛰겠습니다."
fi

# 5. Git 상태 확인
print_step "Git 상태 확인 중..."

if git rev-parse --git-dir > /dev/null 2>&1; then
    # 미커밋된 변경사항 확인
    if [[ -n $(git status --porcelain) ]]; then
        print_warning "미커밋된 변경사항이 있습니다:"
        git status --short
        echo ""
        read -p "변경사항을 커밋하고 푸시하시겠습니까? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            print_step "변경사항 커밋 중..."
            git add docker-compose.coolify.yml COOLIFY_DEPLOYMENT_GUIDE.md DEPLOYMENT_CHECKLIST.md deploy-to-coolify.sh
            git commit -m "feat(deployment): add Coolify deployment configuration and scripts"
            
            print_step "변경사항 푸시 중..."
            git push origin main
            print_success "Git 푸시 완료"
        fi
    else
        print_success "Git 상태 클린"
    fi
else
    print_warning "Git 저장소가 아닙니다."
fi

# 6. 배포 정보 요약
echo ""
print_step "배포 정보 요약"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎯 배포 대상: Enhanced Memory-Vector RAG"
echo "🐳 Docker Compose: docker-compose.coolify.yml"
echo "🌐 Coolify URL: http://165.232.167.204:8000/"
echo ""
echo "📦 배포될 서비스:"
echo "  • mcp-server (포트 8000) - 메인 MCP 서버"
echo "  • chainlit-ui (포트 8501) - 웹 인터페이스"
echo "  • grafana (포트 3000) - 모니터링"
echo "  • prometheus (포트 9090) - 메트릭 수집"
echo ""
echo "🔗 외부 서비스:"
echo "  • Qdrant Cloud - 벡터 데이터베이스"
echo "  • Neo4j Aura - 그래프 데이터베이스"
echo "  • Supabase - 관계형 데이터베이스"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# 7. 최종 확인 및 배포 안내
echo ""
print_step "배포 준비 완료!"
echo ""
echo "🚀 다음 단계를 진행해주세요:"
echo ""
echo "1️⃣  Coolify 대시보드 접속:"
echo "   👉 http://165.232.167.204:8000/"
echo ""
echo "2️⃣  새 리소스 생성:"
echo "   • New Resource → Git Repository"
echo "   • Build Pack: Docker Compose"
echo "   • Docker Compose Location: docker-compose.coolify.yml"
echo ""
echo "3️⃣  환경 변수 설정:"
echo "   📋 COOLIFY_DEPLOYMENT_GUIDE.md 파일의 환경 변수 섹션 참조"
echo ""
echo "4️⃣  배포 시작:"
echo "   • Deploy 버튼 클릭"
echo "   • 로그 모니터링"
echo ""
echo "5️⃣  배포 후 테스트:"
echo "   📋 DEPLOYMENT_CHECKLIST.md 파일의 테스트 섹션 참조"
echo ""

print_success "배포 스크립트 실행 완료!"
echo ""
echo "💡 추가 도움이 필요하시면 다음 문서들을 참조해주세요:"
echo "   📖 COOLIFY_DEPLOYMENT_GUIDE.md - 상세 배포 가이드"
echo "   ✅ DEPLOYMENT_CHECKLIST.md - 배포 체크리스트"
echo ""
echo "🎉 성공적인 배포를 위해 화이팅입니다!"