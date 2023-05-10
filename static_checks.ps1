Write-Host("black  -------------------------------------------------------------------------------------------")
black .
if ($LASTEXITCODE -ne 0)
{
    throw 'Verification faied!'
}
Write-Host("pylint -------------------------------------------------------------------------------------------")
pylint .
if ($LASTEXITCODE -ne 0)
{
    throw 'Verification faied!'
}
Write-Host("mypy   -------------------------------------------------------------------------------------------")
mypy .
if ($LASTEXITCODE -ne 0)
{
    throw 'Verification faied!'
}
Write-Host("pytest -------------------------------------------------------------------------------------------")
pytest --cov-report=term --cov-report=html:cov_html --cov=lib.database --cov=twitter.twitter_api test/
if ($LASTEXITCODE -ne 0)
{
    throw 'Verification faied!'
}
