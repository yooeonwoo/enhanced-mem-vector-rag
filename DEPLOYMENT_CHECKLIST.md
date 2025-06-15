# 🚀 Coolify 배포 체크리스트

## ✅ 배포 전 준비사항

### 1. 파일 준비 확인
- [ ] `docker-compose.coolify.yml` 파일 존재 확인
- [ ] `COOLIFY_DEPLOYMENT_GUIDE.md` 문서 확인
- [ ] `.env` 파일에 모든 필수 변수 설정됨
- [ ] Dockerfile들이 올바른 경로에 위치:
  - [ ] `emvr/deployment/dockerfiles/mcp-server.Dockerfile`
  - [ ] `emvr/deployment/dockerfiles/chainlit-ui.Dockerfile`

### 2. 클라우드 서비스 상태 확인
- [ ] **Qdrant Cloud** 접속 가능 (포트 6333)
- [ ] **Neo4j Aura** 접속 가능 (bolt:// 프로토콜)
- [ ] **Supabase** 접속 가능 (HTTPS API)
- [ ] **OpenAI API** 키 유효성 확인
- [ ] **Tavily API** 키 유효성 확인
- [ ] **Mem0 API** 키 유효성 확인

## 🔧 Coolify 설정 단계

### 1단계: 프로젝트 생성
- [ ] Coolify 대시보드 접속: http://165.232.167.204:8000/
- [ ] "New Resource" → "Git Repository" 선택
- [ ] GitHub 저장소 연결 또는 URL 입력
- [ ] Branch: `main` 선택
- [ ] Build Pack: `Docker Compose` 선택

### 2단계: Docker Compose 설정
- [ ] Docker Compose Location: `docker-compose.coolify.yml` 입력
- [ ] "Raw Compose Deployment" 옵션 체크 (권장)
- [ ] "Preserve Repository During Deployment" 체크

### 3단계: 환경 변수 설정
**필수 API 키들:**
- [ ] `OPENAI_API_KEY`
- [ ] `TAVILY_API_KEY`
- [ ] `MEM0_API_KEY`

**데이터베이스 연결:**
- [ ] `QDRANT_URL`
- [ ] `QDRANT_API_KEY`
- [ ] `NEO4J_URI`
- [ ] `NEO4J_USERNAME`
- [ ] `NEO4J_PASSWORD`
- [ ] `SUPABASE_URL`
- [ ] `SUPABASE_KEY`

**기타 설정:**
- [ ] `EMBEDDING_MODEL`
- [ ] `LLM_MODEL`
- [ ] `JWT_SECRET_KEY`
- [ ] `LOG_LEVEL`
- [ ] `GRAFANA_ADMIN_PASSWORD` (선택사항)

### 4단계: 도메인 설정 (선택사항)
- [ ] MCP Server용 도메인 설정
- [ ] Chainlit UI용 도메인 설정
- [ ] Grafana용 도메인 설정 (모니터링)

## 🚀 배포 실행

### 배포 시작
- [ ] "Deploy" 버튼 클릭
- [ ] 배포 로그 실시간 모니터링
- [ ] 각 서비스 빌드 성공 확인
- [ ] 헬스체크 통과 확인

### 배포 후 검증
- [ ] **MCP Server** 헬스체크: `GET /health`
- [ ] **Chainlit UI** 접속 테스트
- [ ] **Grafana** 대시보드 접속 (선택사항)
- [ ] **Prometheus** 메트릭 수집 확인 (선택사항)

## 🔍 배포 후 테스트

### 기능 테스트
- [ ] Chainlit UI를 통한 채팅 테스트
- [ ] MCP Server API 엔드포인트 테스트
- [ ] 벡터 검색 기능 테스트 (Qdrant)
- [ ] 그래프 쿼리 기능 테스트 (Neo4j)
- [ ] 메모리 저장/검색 테스트 (Mem0)

### 성능 테스트
- [ ] 응답 시간 측정
- [ ] 메모리 사용량 확인
- [ ] CPU 사용량 확인
- [ ] 동시 연결 테스트

## 🆘 문제 해결

### 일반적인 오류들
- [ ] **빌드 실패**: Dockerfile 경로 및 의존성 확인
- [ ] **헬스체크 실패**: 포트 설정 및 서비스 상태 확인
- [ ] **환경 변수 오류**: 모든 필수 변수 설정 확인
- [ ] **데이터베이스 연결 실패**: 클라우드 서비스 상태 및 인증 정보 확인

### 로그 확인 위치
- [ ] Coolify 대시보드 → 서비스별 "Logs" 탭
- [ ] 컨테이너 내부 로그: `/app/logs/` 디렉토리
- [ ] 시스템 로그: Coolify 호스트 서버

## 📊 모니터링 설정

### Grafana 설정 (선택사항)
- [ ] 관리자 계정으로 로그인
- [ ] 데이터소스 추가 (Prometheus)
- [ ] 대시보드 import 또는 생성
- [ ] 알림 설정 (선택사항)

### 로그 수집
- [ ] Application 로그 수집 설정
- [ ] Error 로그 알림 설정
- [ ] Performance 메트릭 모니터링

## ⚡ 빠른 배포 명령어

```bash
# 1. 프로젝트 클론 (이미 완료)
# git clone [your-repo-url]
# cd enhanced-mem-vector-rag

# 2. 환경 변수 확인
cat .env

# 3. Docker Compose 구성 확인
cat docker-compose.coolify.yml

# 4. 로컬 테스트 (선택사항)
docker-compose -f docker-compose.coolify.yml config

# 5. Git 커밋 및 푸시 (변경사항이 있는 경우)
git add docker-compose.coolify.yml COOLIFY_DEPLOYMENT_GUIDE.md DEPLOYMENT_CHECKLIST.md
git commit -m "feat(deployment): add Coolify deployment configuration"
git push origin main
```

## 🎯 성능 최적화 팁

### 리소스 할당 권장사항
- **MCP Server**: 1GB RAM, 0.5 CPU
- **Chainlit UI**: 512MB RAM, 0.25 CPU
- **Grafana**: 256MB RAM, 0.1 CPU
- **Prometheus**: 512MB RAM, 0.2 CPU

### 네트워크 최적화
- [ ] CDN 설정 (정적 파일용)
- [ ] 압축 활성화
- [ ] 캐싱 헤더 설정

### 보안 설정
- [ ] JWT Secret 강화
- [ ] API 키 주기적 교체
- [ ] HTTPS 강제 설정
- [ ] 방화벽 규칙 설정

---

이 체크리스트를 따라가시면 성공적으로 배포할 수 있습니다! 🚀