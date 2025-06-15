# Enhanced Memory-Vector RAG - Coolify 배포 가이드

## 🚀 개요

이 가이드는 Enhanced Memory-Vector RAG 시스템을 Coolify (http://165.232.167.204:8000/)에 배포하는 완전한 단계별 가이드입니다.

**주요 특징:**
- 클라우드 서비스 활용 (Qdrant Cloud, Neo4j Aura, Supabase Cloud)
- 최소한의 코드 변경으로 배포 가능
- 헬스체크 및 모니터링 포함
- 프로덕션 준비된 설정

## 📋 1단계: 환경 변수 설정

### 필수 환경 변수 (Coolify UI에서 설정)

Coolify 대시보드에서 다음 환경 변수들을 설정해야 합니다:

#### **API 키들**
```bash
# OpenAI API 키 (필수)
OPENAI_API_KEY=your_openai_api_key_here

# Tavily 검색 API 키
TAVILY_API_KEY=your_tavily_api_key_here

# Mem0 API 키
MEM0_API_KEY=your_mem0_api_key_here
```

#### **데이터베이스 연결**
```bash
# Qdrant Cloud 설정
QDRANT_URL=your_qdrant_cluster_url_here
QDRANT_API_KEY=your_qdrant_api_key_here

# Neo4j Aura 설정
NEO4J_URI=your_neo4j_uri_here
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your_neo4j_password_here

# Supabase Cloud 설정
SUPABASE_URL=your_supabase_url_here
SUPABASE_KEY=your_supabase_anon_key_here
```

#### **모델 및 설정**
```bash
# 임베딩 모델
EMBEDDING_MODEL=BAAI/bge-small-en-v1.5

# LLM 모델
LLM_MODEL=o4-mini

# 문서 처리 설정
DEFAULT_CHUNK_SIZE=1000
DEFAULT_CHUNK_OVERLAP=200

# Mem0 설정
USE_MEM0=true
MEM0_MEMORY_ID=yoo-agent

# 로깅 레벨
LOG_LEVEL=INFO

# 보안 키 (새로 생성 권장)
JWT_SECRET_KEY=your_jwt_secret_key_here
TOKEN_EXPIRY_MINUTES=60

# Grafana 관리자 비밀번호 (선택사항)
GRAFANA_ADMIN_PASSWORD=your_secure_password_here
```

### 환경 변수 설정 방법

1. **Coolify 대시보드 접속**: http://165.232.167.204:8000/
2. **프로젝트 선택** 후 **Environment Variables** 탭 클릭
3. **위 변수들을 하나씩 추가**:
   - Variable Name: 변수명 입력
   - Variable Value: 값 입력
   - **Build Time**: 빌드 시에만 필요한 변수는 체크
   - **Runtime**: 런타임에 필요한 변수는 체크 (대부분)

## 📦 2단계: 프로젝트 설정

### Git 저장소 연결

1. **New Resource** → **Git Repository** 선택
2. **Repository URL** 입력 또는 GitHub 앱 연결
3. **Branch**: `main` 선택
4. **Build Pack**: `Docker Compose` 선택
5. **Docker Compose Location**: `docker-compose.coolify.yml` 지정

### 서비스 설정

배포될 서비스들:
- **mcp-server** (포트 8000) - 메인 MCP 서버
- **chainlit-ui** (포트 8501) - 웹 UI
- **grafana** (포트 3000) - 모니터링 (선택사항)
- **prometheus** (포트 9090) - 메트릭 (선택사항)

## 🔧 3단계: 배포 설정

### 도메인 설정

각 서비스에 대해 도메인을 설정할 수 있습니다:
- **mcp-server**: `api.yourdomain.com`
- **chainlit-ui**: `chat.yourdomain.com` 또는 메인 도메인
- **grafana**: `monitor.yourdomain.com`

### SSL/TLS 인증서

Coolify가 자동으로 Let's Encrypt 인증서를 생성하고 관리합니다.

### 리소스 제한

권장 설정:
```yaml
# 각 서비스별 리소스 제한 (Coolify UI에서 설정)
mcp-server:
  memory: 1GB
  cpu: 0.5

chainlit-ui:
  memory: 512MB
  cpu: 0.25

grafana:
  memory: 256MB
  cpu: 0.1

prometheus:
  memory: 512MB
  cpu: 0.2
```

## 🚀 4단계: 배포 실행

### 배포 순서

1. **Environment Variables** 모두 설정 확인
2. **Deploy** 버튼 클릭
3. **로그 모니터링**으로 배포 진행상황 확인
4. **헬스체크** 통과 확인

### 배포 후 확인사항

1. **서비스 상태 확인**:
   ```bash
   # 각 서비스의 헬스체크 엔드포인트 확인
   curl https://your-mcp-server-domain/health
   curl https://your-chainlit-domain/
   ```

2. **로그 확인**:
   - Coolify 대시보드에서 각 서비스의 로그 확인
   - 에러나 경고 메시지 확인

3. **기능 테스트**:
   - Chainlit UI 접속 테스트
   - MCP 서버 API 엔드포인트 테스트
   - 데이터베이스 연결 확인

## 🔍 5단계: 모니터링 및 유지보수

### 로그 모니터링

- **Application Logs**: Coolify 대시보드에서 실시간 로그 확인
- **Error Tracking**: 에러 로그 모니터링 및 알림 설정
- **Performance**: Grafana 대시보드로 성능 메트릭 확인

### 백업 전략

1. **환경 변수**: Coolify에서 환경 변수 백업
2. **코드**: Git 저장소에 모든 코드 백업
3. **데이터**: 클라우드 서비스 자체 백업 기능 활용
   - Qdrant Cloud: 자동 백업
   - Neo4j Aura: 자동 백업
   - Supabase: 자동 백업

### 업데이트 프로세스

1. **Git Push**: 코드 변경사항을 main 브랜치에 푸시
2. **Auto Deploy**: Coolify가 자동으로 새 배포 감지 및 실행
3. **Health Check**: 배포 후 헬스체크 자동 실행
4. **Rollback**: 문제 발생 시 이전 버전으로 롤백 가능

## ⚠️ 주의사항

### 보안

1. **환경 변수**: API 키와 비밀번호는 절대 코드에 하드코딩하지 말 것
2. **접근 제한**: 필요한 경우 IP 허용 목록 설정
3. **정기 업데이트**: 보안 패치 정기 적용

### 성능

1. **리소스 모니터링**: CPU, 메모리 사용량 정기 확인
2. **스케일링**: 트래픽 증가 시 리소스 증설
3. **캐싱**: 필요한 경우 캐싱 레이어 추가 고려

### 비용 최적화

1. **클라우드 서비스**: 사용량에 따른 요금제 최적화
2. **리소스 할당**: 불필요한 리소스 제거
3. **모니터링**: 사용량 추적 및 최적화

## 🆘 문제 해결

### 일반적인 문제들

1. **서비스 시작 실패**:
   - 환경 변수 확인
   - 데이터베이스 연결 상태 확인
   - 도커 이미지 빌드 로그 확인

2. **헬스체크 실패**:
   - 포트 설정 확인
   - 서비스 내부 상태 확인
   - 네트워크 연결 확인

3. **성능 문제**:
   - 리소스 사용량 확인
   - 데이터베이스 쿼리 최적화
   - 캐싱 전략 검토

### 지원 연락처

- **Coolify 문서**: https://coolify.io/docs
- **GitHub Issues**: 프로젝트 저장소 이슈 페이지
- **커뮤니티**: Coolify Discord 또는 포럼

---

이 가이드를 따라하시면 성공적으로 Enhanced Memory-Vector RAG 시스템을 Coolify에 배포할 수 있습니다!