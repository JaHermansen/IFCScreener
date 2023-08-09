@echo off

REM Display the logo and introduction
echo.
echo  VV          VV  DDDDD       CCCCC
echo   VV        VV   DDDDDD     CCCCC
echo    VV      VV    DDD DDD   CCCCC
echo     VV    VV     DDD  DDD  C
echo      VV  VV      DDD  DDD  C
echo       VV V       DDD DDD   CCCCC
echo        VV        DDDDDD     CCCCC
echo        VV        DDDDD       CCCCC

echo   Welcome to IFC Screener
echo   ============================
echo.
echo The app is now running...
echo Press Ctrl+C to shut down the app.

REM Run the Streamlit app
streamlit run Homepage.py --server.port 8888
