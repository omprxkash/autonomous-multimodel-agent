Add-Type -AssemblyName System.Speech
$s = New-Object System.Speech.Synthesis.SpeechSynthesizer
$s.SelectVoice("Microsoft David Desktop")
$s.Rate = 0
$out = "d:\AI\Business\run-3\video\assets\vo-founder.wav"
$s.SetOutputToWaveFile($out)
$text = @"
I'm the founder of WideTally. If you publish books beyond Amazon, you know the morning ritual: five dashboards, five logins, and a spreadsheet that stopped keeping up two books ago.
We didn't fix that with another cloud subscription. Amazon has confirmed there is no A P I for author royalties — every tracker lives off the same report files you already download. So WideTally simply reads those files, on your machine. Nothing uploads. No password to share. No server to go down.
You get one ledger: every store, every book, every series — and ad spend measured against royalties, not list price. It costs fifty nine dollars, once. Format updates are nineteen dollars a year, and optional.
Authors have enough subscriptions. Try the demo — it runs on sample data, so you can judge it before you trust it.
"@
$s.Speak($text)
$s.Dispose()
Write-Output "wrote $out"
