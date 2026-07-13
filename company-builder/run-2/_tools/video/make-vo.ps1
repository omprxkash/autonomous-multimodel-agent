# Generate founder voiceover via Windows built-in TTS (System.Speech).
# Output: run-2/video/assets/vo-founder.wav
Add-Type -AssemblyName System.Speech
$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer
$voices = $synth.GetInstalledVoices() | ForEach-Object { $_.VoiceInfo.Name }
Write-Host "Installed voices: $($voices -join ', ')"
# Prefer a male US voice if present (David), else default
$pick = $voices | Where-Object { $_ -match "David" } | Select-Object -First 1
if ($pick) { $synth.SelectVoice($pick); Write-Host "Using voice: $pick" }
$synth.Rate = 0   # default rate; -1 produced a 114s read, too slow against footage

$script = @'
I'm building DueCrew. Let me explain it in about a minute, without the pitch voice.

If you hold a trade license, your right to work has expiration dates. Your license. Your insurance certificates. Your bond. Your continuing education hours. Miss one, and the state calls your work unlicensed. A general contractor can hold your money. In one documented case, a single expired certificate cost a subcontractor eleven days, and forty seven thousand dollars.

Most of the people this happens to work solo. No office manager. The dates live in a glovebox, and in the back of your head.

DueCrew is one screen that answers one question: am I good to work. Green, amber, red. It knows your state's rules. It counts your C E hours against what's actually required. And it gets louder as a date gets closer. From ninety days out, down to the day before.

It is not a suite. There is no scheduling, no dispatch, no invoicing. Small contractors keep telling the software industry they don't want another suite. We built the one thing instead.

Twelve dollars a month. Less than a single delinquent renewal fee.

What you're seeing today is a demo, and I'd rather tell you that than fake it. The research behind it is public. Every claim has a source. If this should exist, join the waitlist. If you think I'm wrong, tell me why. That's worth more than a sign up.
'@

$out = Join-Path $PSScriptRoot "..\..\video\assets\vo-founder.wav"
$out = [System.IO.Path]::GetFullPath($out)
$synth.SetOutputToWaveFile($out)
$synth.Speak($script)
$synth.Dispose()
Write-Host "Wrote $out"
