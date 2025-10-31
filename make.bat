@echo off

SET src_path=src
SET project_path=%src_path%/kk_scene_timeline_info
SET mypylint=mypy %project_path% --ignore-missing-imports --no-warn-unused-ignores --warn-redundant-casts --warn-unused-ignores --pretty --show-error-codes --check-untyped-defs
SET from_bin=0
SET from_release=0

IF /I "%1"==".DEFAULT_GOAL " GOTO .DEFAULT_GOAL 
IF /I "%1"=="pretty" GOTO pretty
IF /I "%1"=="format" GOTO format
IF /I "%1"=="lint" GOTO lint
IF /I "%1"=="test" GOTO test
IF /I "%1"=="bin" GOTO bin
IF /I "%1"=="run" GOTO run
IF /I "%1"=="release" GOTO release
GOTO error

:.DEFAULT_GOAL 
	CALL make.bat =
	CALL make.bat all
	GOTO :EOF

:pretty
	ruff format %project_path%
	GOTO :EOF

:format
	ruff format %project_path%
	ruff check --fix
	%mypylint%
	GOTO :EOF

:lint
	ruff check
	%mypylint%
	GOTO :EOF

:test
	pytest %project_path%
	GOTO :EOF

:run
	python %src_path%/main.py
	GOTO :EOF

:bin
	cxfreeze build
	IF %from_release%==1 (
		SET from_bin=1
		GOTO release
	) ELSE (
		GOTO :EOF
	)

:release
	IF %from_bin%==0 (
		ruff check
		%mypylint%
		pytest %project_path%
		SET from_release=1
		GOTO bin
	)
	python %src_path%/make_release.py
	GOTO :EOF

:error
    IF "%1"=="" (
        ECHO make: *** No targets specified and no makefile found.  Stop.
    ) ELSE (
        ECHO make: *** No rule to make target '%1%'. Stop.
    )
    GOTO :EOF
