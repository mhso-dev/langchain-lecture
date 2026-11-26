# 팀 활동지 · 동료가 다시 실행할 수 있는 Python 예제

**준비물**은 앞에서 완성한 Python 예제 한 개, [시작 문서 cases.md](cases.md), Git을 쓸 수 있는 터미널, 두 사람이 브랜치를 올리고 PR을 병합할 수 있는 수업용 GitHub 저장소입니다. 이 활동지는 개인 노트나 복사본에 작성하세요. 아래에서 민과 윤은 가상의 짝입니다. 한 사람은 `min`, 다른 사람은 `yun`을 골라 명령과 폴더 이름에 사용하세요. 문법·패턴 중 어느 과정을 들었든 두 역할을 모두 맡을 수 있습니다.

## 예제를 쓰던 폴더를 보존하고 오타만 고치기 (90분)

**준비 20분.** 두 사람만 사용하는 수업용 저장소의 기본 브랜치를 `main`으로 정합니다. 조장이 GitHub에서 루트(최상위 폴더)에 제공받은 `cases.md`를 올려 첫 커밋을 만듭니다. 이어서 루트에 `.gitignore` 파일을 만들고 `.ipynb_checkpoints/` 한 줄을 적어 커밋합니다. Jupyter의 임시 저장 폴더가 팀의 변경 목록에 섞이는 것을 막습니다. 이미 있다면 내용만 확인합니다. GitHub의 **Code**에서 저장소 주소를 복사하세요. 아래 명령의 `팀저장소주소` 자리에는 복사한 주소를 넣습니다. 처음 여는 빈 실습 폴더의 터미널에서 각자 한 번 실행합니다.

```bash
git clone 팀저장소주소 team    # 마지막 단어는 내 컴퓨터에 생길 폴더 이름입니다.
cd team                     # 다음 명령부터 이 폴더에서 실행합니다.
git remote -v               # origin의 주소가 두 사람의 연습 저장소인지 확인합니다.
git status --short --branch
git log -1 --oneline        # 최근 커밋의 짧은 식별자와 제목을 봅니다.
```

작성자 설정이 없는 컴퓨터에서는 `git config user.name "수업용 이름"`, `git config user.email "GitHub에서 사용하는 수업용 이메일"`을 이 폴더에서 한 번 실행합니다. 이메일 공개를 원하지 않으면 GitHub 계정에 설정된 비공개 커밋용 이메일을 사용하세요.

**예제 초안 30분.** 민은 아래 명령을 실행하고 윤은 모든 `min`을 `yun`으로 바꿉니다. 이후 명령도 같은 방식으로 읽으세요.

```bash
git switch -c case/min       # 방금 받은 기준 커밋에서 예제용 브랜치를 만듭니다.
mkdir min                   # 내 예제와 결과를 보관할 폴더입니다.
cp cases.md min/cases.md     # 내 폴더에 기록용 사본을 만듭니다.
```

Jupyter에서 새 Python 3 노트북을 만들고 `min/case.ipynb`로 저장합니다. 이전 단원에서 고른 예제의 입력·계산·출력 셀을 복사하고 필요한 정의도 함께 옮기세요. 새 커널에서 위부터 실행해 같은 출력이 나오는지 확인합니다. `min/cases.md`의 내용은 예제 제목과 **입력 / 기대값 / 실제값** 한 줄로 바꾸세요. 루트의 `cases.md`는 그대로 둡니다. 아직 커밋하지 마세요. `git status --short`에서 `?? min/`이 나타나는지 확인합니다.

**오타 접수 25분.** 짝이 루트 문서의 오타를 알려 왔습니다. 민은 ‘문벙’을 ‘문법’으로, 윤은 ‘정렬 기즌’을 ‘정렬 기준’으로 고칩니다. 아래 명령을 첫 폴더 `team`에서 실행하세요. `../`는 지금 폴더의 상위 폴더입니다.

```bash
git worktree add -b fix/min-type ../spelling main    # main의 파일을 옆 폴더에 펼칩니다.
cd ../spelling
git branch --show-current                           # fix/min-type을 확인합니다.
```

편집기에서 **spelling 쪽** `cases.md`를 열어 자기 오타 하나만 바꾸고 저장합니다. 다음 명령은 두 번째 폴더에서 실행합니다.

```bash
git diff -- cases.md                  # 더해지는 줄과 빠지는 줄을 읽습니다.
git add cases.md                      # 수정한 문서만 다음 기록에 담습니다.
git diff --cached --name-only         # cases.md 한 개여야 합니다.
git commit -m "실습 안내의 오타 수정"
git show --format= --name-only HEAD   # 방금 만든 커밋의 파일 이름을 확인합니다.
cd ../team
git status --short --branch           # case/min에 작성 중인 min/이 남아 있어야 합니다.
```

**인계 15분.** 내 첫 폴더의 브랜치와 미커밋 파일, 둘째 폴더의 브랜치와 방금 기록한 파일을 적으세요. 짝에게 먼저 올릴 오타 브랜치 이름을 말하고 두 폴더를 다음 시간까지 보존합니다.

| 내가 관찰한 항목 | 내 기록 |
|---|---|
| 첫 폴더의 브랜치·미커밋 파일 | |
| 둘째 폴더의 브랜치·커밋한 파일 | |
| 오타 커밋에 예제 초안이 들어 있지 않은 근거 | |

<details><summary>워크트리 모범 기록 보기</summary>
<p>민의 예시입니다. 첫 폴더는 <code>case/min</code>이며 <code>?? min/</code>이 남습니다. 두 번째는 <code>fix/min-type</code>이며 <code>git show --format= --name-only HEAD</code>에 <code>cases.md</code>만 나옵니다. 이 브랜치를 먼저 올리면 동료는 오타만 검토할 수 있습니다.</p>
</details>

## 짝의 리뷰를 반영하고 충돌 해결하기 (120분)

**두 오타 올리기 20분.** 각자 어제 만든 두 번째 폴더에서 `git push -u origin fix/min-type`을 실행합니다. 윤은 `fix/yun-type`을 올립니다. `-u`는 현재 브랜치가 원격의 어느 브랜치를 따라갈지 저장합니다. GitHub에서 **Pull requests → New pull request**를 열어 합칠 곳(base)을 `main`, 제안할 쪽(compare)을 자기 오타 브랜치로 선택합니다. 변경 파일에서 고친 오타 한 곳을 확인하고 PR을 엽니다. 짝의 PR을 서로 확인한 뒤 두 오타 PR을 차례로 병합합니다.

**예제 PR 열기 25분.** 첫 폴더 `team`으로 돌아갑니다. 아직 `case/min` 또는 `case/yun`인지 `git branch --show-current`로 확인합니다. 두 사람 모두 **루트** `cases.md`에서 `확인할 것: 입력과 실제값` 줄을 수정하세요. 민은 끝에 `, 단위`를, 윤은 끝에 `, 실행 순서`를 붙입니다. 두 사람이 같은 커밋의 같은 줄을 수정해야 뒤에서 충돌을 관찰할 수 있습니다. 이 시점에는 두 사람 모두 원격의 새 main을 자기 브랜치에 가져오지 않습니다.

```bash
git add min/case.ipynb min/cases.md cases.md   # 재현할 예제·내 기록·공통 안내를 고릅니다.
git diff --cached --name-only
git commit -m "Python 예제와 재현 입력 추가"
git push -u origin case/min
```

각자 **base = main**, **compare = 자기 예제 브랜치**로 두 번째 PR을 엽니다. 본문에 노트북 경로, 처음 실행할 입력, 기대값을 적습니다. 두 예제 PR 모두 열린 상태로 다음 단계에 들어갑니다.

**코드 리뷰와 수정 30분.** 짝의 예제 PR에서 **Files changed**를 열고 개인 기록 파일의 구체적인 줄에 의견을 남깁니다. 문법 예제를 받았다면 경계값 입력, 패턴 예제라면 기준을 바꾼 입력을 하나 제안하세요. 의견을 여러 개 작성했다면 리뷰 제출까지 마쳐야 상대에게 전달됩니다. 작성자는 새 입력을 자기 노트북에서 실행하고, 두 번째 사례를 개인 기록에 추가합니다. 이미 열린 자기 예제 브랜치에서 변경한 파일을 다시 `add → commit → push`합니다. 같은 PR에 커밋이 더해졌는지 두 사람 모두 파일 차이에서 확인합니다.

<details><summary>리뷰와 회신 예시 보기</summary>
<p>문법 예제에 남긴 리뷰: “1시간 2분 3초는 3723초가 되네요. 세 값이 모두 0일 때 결과도 확인할 수 있을까요?” 작성자 회신: “두 번째 입력을 0시간 0분 0초로 실행했습니다. 결과 0초를 min/cases.md에 추가했습니다.”</p>
<p>패턴 예제에 남길 수 있는 리뷰: “두 단어의 길이가 같을 때 원래 순서를 유지하는지 볼 수 있을까요?” 작성자는 실제로 사용한 단어, 기준, 결과 순서를 회신합니다. 두 댓글 모두 제출할 형식을 보여 주는 예시입니다.</p>
</details>

**충돌 해결 30분.** 짝은 민의 예제 PR을 먼저 승인하고 병합합니다. 이제 `main`에는 민의 ‘단위’가 있고, 윤의 예제 브랜치에는 ‘실행 순서’가 있습니다. 윤은 자기 `team` 폴더에서 다음을 실행하고 민은 화면의 두 줄을 함께 읽습니다.

```bash
git status --short --branch   # case/yun에서 미커밋 수정이 없는지 봅니다.
git fetch origin             # 팀의 새 커밋을 받아 origin/main을 갱신합니다.
git merge origin/main        # 새 기본 버전을 현재 예제 브랜치에 합칩니다.
git status --short           # UU cases.md는 양쪽이 바꿔 합의가 필요한 파일입니다.
```

`cases.md`를 열어 `<<<<<<<`와 `=======` 사이에 있는 현재 브랜치의 줄, `=======`와 `>>>>>>>` 사이에 있는 가져온 줄을 읽으세요. 두 조건을 살린 문장 하나를 남기고 표식 세 줄을 지웁니다. 두 사람의 예제 폴더와 오타 수정이 유지됐는지도 봅니다. 폴더·브랜치·충돌 파일이 활동지와 다르면, 방금 충돌한 병합 중에 `git merge --abort`로 시도 전으로 돌아가 `git status`부터 대조하세요.

```bash
git add cases.md                               # 두 사람이 고른 문장을 해결안으로 등록합니다.
git diff --cached --check                      # 남은 충돌 표식 등을 검사합니다.
git commit -m "재실행 안내에 단위와 실행 순서를 모두 보존"
git push origin case/yun
```

민이 윤의 PR에서 해결된 문장과 두 예제를 확인하고 승인한 뒤 병합합니다.

**동기화와 재실행 15분.** 각자 `team` 폴더에서 다음을 실행합니다.

```bash
git status --short                   # 비어 있으면 저장할 수정이 남지 않은 상태입니다.
git switch main
git pull --ff-only origin main        # 내 main을 팀의 최신 main까지 앞으로 이동합니다.
git log -1 --oneline
git -C ../spelling status --short    # 둘째 폴더에도 미커밋 수정이 없는지 확인합니다.
git worktree remove ../spelling      # 끝난 작업 폴더를 정리합니다.
git worktree list                    # team의 main 작업 폴더가 남습니다.
```

`--ff-only`가 거절되면 내 `main`에 팀과 다른 커밋이 있는 상태일 수 있습니다. `git log --oneline --graph --all -8`로 두 기록을 먼저 살펴보세요. 이어서 짝이 만든 `case.ipynb`를 갱신한 폴더에서 열고 새 커널로 실행합니다. 기본 입력과 추가 입력이 모두 재현되는지 직접 확인합니다.

| 제출할 증거 | 내 기록 |
|---|---|
| 내가 올린 예제 PR 주소 | |
| 동료 PR에서 내가 쓴 리뷰의 링크 | |
| 받은 리뷰와 이를 반영한 커밋의 짧은 식별자 | |
| 충돌 직전 두 줄과 두 조건을 모두 살린 해결 문장 | |
| 동료 예제를 다시 실행한 입력·기대값·실제값 | |

<details><summary>마지막 확인 예시 보기</summary>
<p>공통 문서는 “확인할 것: 입력과 실제값, 단위, 실행 순서”입니다. 두 개인 폴더의 예제와 결과 기록이 main에 함께 있어야 합니다. 예를 들어 동료가 0시간 0분 0초를 0초로 기록했다면, 내 컴퓨터에서도 그 입력을 넣어 실제로 본 값을 남깁니다. PR 주소와 커밋 식별자는 팀에서 생성한 실제 값으로 채우세요.</p>
</details>

명령과 리뷰 조작 참고 문서 · [Git worktree](https://git-scm.com/docs/git-worktree) · [GitHub에서 파일 변경을 검토하는 방법](https://docs.github.com/en/pull-requests/how-tos/review-pull-requests/reviewing-proposed-changes-in-a-pull-request)
