@Echo off
setlocal ENABLEDELAYEDEXPANSION

:: Possible paths to check for the installation
set inkscapePath1="C:\Program Files\Inkscape\bin\inkscape.exe"
set inkscapePath2="C:\Program Files\Inkscape\inkscape.exe"
set inkscapePath3="C:\Program Files (x86)\Inkscape\bin\inkscape.exe"
set inkscapePath4="C:\Program Files (x86)\Inkscape\inkscape.exe"


if exist %inkscapePath1% (
	set inkscapePath=%inkscapePath1%
) else (
	if exist %inkscapePath2% (
		set inkscapePath=%inkscapePath2%
	) else (
		if exist %inkscapePath3% (
			set inkscapePath=%inkscapePath3%
		) else (
			if exist %inkscapePath4% (
				set inkscapePath=%inkscapePath4%
			) else (
				echo Can't find Inkscape installation, aborting.
				GOTO end
			)
		)
	)
)


set validInput1=svg
set validInput2=pdf
set validInput3=eps
set validInput4=emf
set validInput5=wmf

set validOutput1=eps
set validOutput2=pdf
set validOutput3=png
set validOutput4=svg

FOR /F "tokens=* USEBACKQ" %%g IN (`%inkscapePath% --version`) do (SET "inkscapeVersion=%%g")
set /a inkscapeMajorVersion=%inkscapeVersion:~9,1%

echo.
echo This script allows you to convert all files in this folder from one file type to another
echo Running with %inkscapeVersion%
echo (type q to quit at any question)
echo.

set valid=0
echo Allowed file types for source: %validInput1%, %validInput2%, %validInput3%, %validInput4%, %validInput5%

:whileInNotCorrect
	set /p sourceType=What file type do you want to use as a source? 
	if "%sourceType%" EQU "%validInput1%" set valid=1
	if "%sourceType%" EQU "%validInput2%" set valid=1
	if "%sourceType%" EQU "%validInput3%" set valid=1
	if "%sourceType%" EQU "%validInput4%" set valid=1
	if "%sourceType%" EQU "%validInput5%" set valid=1
	if "%sourceType%" EQU "q" exit /b
	if %valid% EQU 0 (
		echo Invalid input! Please use one of the following: %validInput1%, %validInput2%, %validInput3%, %validInput4%, %validInput5%
		goto :whileInNotCorrect
	)
	
echo.

set valid=0
echo Allowed file types for output: %validOutput1%, %validOutput2%, %validOutput3%, %validOutput4%      
:whileOutNotCorrect
	set /p outputType=What file type do you want to convert to? 
	if "%outputType%" EQU "%validOutput1%" set valid=1
	if "%outputType%" EQU "%validOutput2%" set valid=1
	if "%outputType%" EQU "%validOutput3%" set valid=1
	if "%outputType%" EQU "%validOutput4%" set valid=1
	if "%outputType%" EQU "q" exit /b
	if %valid% EQU 0 (
		echo Invalid input! Please use one of the following: %validOutput1%, %validOutput2%, %validOutput3%, %validOutput4% 
		goto :whileOutNotCorrect
	)

if "%outputType%" EQU "%sourceType%" (
	echo Input and Output are the same, no point in doing anything. Exiting...
	exit /b
)

echo.

:: Older inkscape versions need to generate a pdf before generating svgs
if %inkscapeMajorVersion% EQU 0 (
	set toDelOrNot=n
	if "%sourceType%" NEQ "pdf" (
		if "%outputType%" EQU "%validOutput4%" (
			set valid=0
			:whilePdfDelNotCorrect
				set /p toDelOrNot=EPS to SVG also generates pdfs, delete these after conversion? (y/n^) 
				if "%toDelOrNot%" EQU "y" set valid=1
				if "%toDelOrNot%" EQU "n" set valid=1
				if "%toDelOrNot%" EQU "q" exit /b
				if %valid% EQU 0 (
					echo Invalid input! Please type either y or n.
					goto :whilePdfDelNotCorrect
				)
		)
	)
)

:: Set DPI for exported file
:whileNotValidDpiNumber
	set /p dpi=With what dpi should it be exported (e.g. 300)? 
	if "%dpi%" EQU "q" exit /b
	IF %dpi% NEQ +%dpi% (
		echo Invalid input! Please input an actual number.
		goto :whilenotValidDpiNumber
	)
echo.

:: count how many files we need to convert before converting!
set /a total=0
for /R %%i in (*.%sourceType%) do (
	set /a total=total+1
)
echo Conversion started. Will do %total% file(s).

echo.

set /a count=0
:: Running through all files found with the defined ending
if %inkscapeMajorVersion% NEQ 0 (
	:: Inkscape 1.0 and newer
	for /R %%i in (*.%sourceType%) do (
		set /a count=count+1
		
		:: Create out folder if it does not exist
		if not exist %%~di%%~piout mkdir %%~di%%~piout
		
		echo %%i -^> %%~di%%~piout\%%~ni.%outputType% ^[!count!/%total%^]
		
		%inkscapePath% --batch-process --export-filename="%%~di%%~piout\%%~ni.%outputType%" --export-dpi=%dpi% "%%i"
	)
) else (
	:: Inkscape 0.9.x and older
	for /R %%i in (*.%sourceType%) do (
		set /a count=count+1
		
		echo %%i -^> %%~di%%~piout\%%~ni.%outputType% ^[!count!/%total%^]
		
		if "%outputType%" NEQ "%validOutput4%" (
			%inkscapePath% --without-gui --file="%%i" --export-%outputType%="%%~di%%~piout\%%~ni.%outputType%" --export-dpi=%dpi%
		) else (
			if "%sourceType%" NEQ "pdf" (
				%inkscapePath% --without-gui --file="%%i" --export-pdf="%%~di%%~piout\%%~ni.pdf" --export-dpi=%dpi%
			)
			%inkscapePath% --without-gui -z -f "out\%%~ni.pdf" -l "%%~di%%~piout\%%~ni.%validOutput4%"
			if "%toDelOrNot%" EQU "y" (
				del "%%~ni.pdf" /f /q
			)
		)
	)
)

echo.
echo %count% file(s) converted from %sourceType% to %outputType%! (Saved in out folder)
echo.

:end
pause