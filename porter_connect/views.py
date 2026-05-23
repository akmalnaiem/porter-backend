from django.http import HttpResponse


def home(request):
    return HttpResponse("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
    <title>Porter Backend — JARVIS Interface</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700;800;900&family=Rajdhani:wght@300;400;500;600;700&family=Share+Tech+Mono&display=swap" rel="stylesheet">
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    fontFamily: {
                        orbitron: ['Orbitron', 'sans-serif'],
                        rajdhani: ['Rajdhani', 'sans-serif'],
                        mono: ['Share Tech Mono', 'monospace'],
                    },
                    colors: {
                        jarvis: {
                            cyan: '#00e5ff',
                            glow: '#00f7ff',
                            arc: '#4dd0e1',
                            dim: '#0a1628',
                            panel: 'rgba(6, 24, 44, 0.72)',
                        }
                    }
                }
            }
        }
    </script>
    <style>
        :root {
            --cyan: #00e5ff;
            --glow: #00f7ff;
            --arc: #26c6da;
            --green: #00ff9d;
            --amber: #ffb300;
            --red: #ff3d5a;
            --bg-deep: #010408;
            --panel: rgba(4, 18, 32, 0.85);
        }

        * { box-sizing: border-box; }

        html {
            scroll-behavior: smooth;
        }

        body {
            font-family: 'Rajdhani', sans-serif;
            background: var(--bg-deep);
            color: #c8f4ff;
            min-height: 100vh;
            min-height: 100dvh;
            overflow-x: hidden;
        }

        /* Ambient layers */
        .bg-layer {
            position: fixed;
            inset: 0;
            pointer-events: none;
            z-index: 0;
        }

        .bg-radial {
            background:
                radial-gradient(ellipse 80% 50% at 50% -10%, rgba(0, 120, 180, 0.35) 0%, transparent 55%),
                radial-gradient(ellipse 60% 40% at 80% 100%, rgba(0, 229, 255, 0.08) 0%, transparent 50%),
                radial-gradient(ellipse 50% 30% at 10% 80%, rgba(0, 100, 255, 0.06) 0%, transparent 45%),
                linear-gradient(180deg, #020810 0%, #000306 50%, #000000 100%);
        }

        .hex-grid {
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='56' height='100' viewBox='0 0 56 100'%3E%3Cpath d='M28 0L56 16v32L28 64 0 48V16z' fill='none' stroke='%2300e5ff' stroke-opacity='0.04'/%3E%3C/svg%3E");
            background-size: 56px 100px;
            opacity: 0.9;
        }

        .scan-line {
            position: absolute;
            left: 0;
            right: 0;
            height: 2px;
            background: linear-gradient(90deg, transparent, var(--glow), transparent);
            box-shadow: 0 0 20px var(--glow), 0 0 40px var(--glow);
            animation: scanDown 6s linear infinite;
            opacity: 0.35;
        }

        @keyframes scanDown {
            0% { top: -2%; }
            100% { top: 102%; }
        }

        /* HUD frame */
        .hud-frame {
            position: relative;
            background: var(--panel);
            border: 1px solid rgba(0, 229, 255, 0.22);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            box-shadow:
                0 0 0 1px rgba(0, 247, 255, 0.05) inset,
                0 0 40px rgba(0, 229, 255, 0.08),
                0 25px 80px rgba(0, 0, 0, 0.5);
        }

        .hud-frame::before {
            content: '';
            position: absolute;
            inset: -1px;
            border-radius: inherit;
            padding: 1px;
            background: linear-gradient(135deg,
                rgba(0, 247, 255, 0.6) 0%,
                transparent 25%,
                transparent 75%,
                rgba(0, 255, 157, 0.4) 100%);
            -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
            mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
            -webkit-mask-composite: xor;
            mask-composite: exclude;
            pointer-events: none;
            opacity: 0.7;
        }

        .corner-bracket {
            position: absolute;
            width: clamp(24px, 4vw, 48px);
            height: clamp(24px, 4vw, 48px);
            border-color: var(--cyan);
            opacity: 0.7;
        }
        .corner-bracket.tl { top: 8px; left: 8px; border-top: 2px solid; border-left: 2px solid; }
        .corner-bracket.tr { top: 8px; right: 8px; border-top: 2px solid; border-right: 2px solid; }
        .corner-bracket.bl { bottom: 8px; left: 8px; border-bottom: 2px solid; border-left: 2px solid; }
        .corner-bracket.br { bottom: 8px; right: 8px; border-bottom: 2px solid; border-right: 2px solid; }

        /* Arc reactor */
        .arc-reactor {
            position: relative;
            width: clamp(140px, 28vw, 220px);
            height: clamp(140px, 28vw, 220px);
        }

        .arc-ring {
            position: absolute;
            inset: 0;
            border-radius: 50%;
            border: 2px solid transparent;
        }

        .arc-ring-1 {
            border-color: rgba(0, 229, 255, 0.35);
            animation: spin 12s linear infinite;
        }

        .arc-ring-2 {
            inset: 12%;
            border-color: rgba(0, 247, 255, 0.5);
            border-style: dashed;
            animation: spinReverse 8s linear infinite;
        }

        .arc-ring-3 {
            inset: 22%;
            border: 1px solid rgba(0, 255, 157, 0.3);
            box-shadow: 0 0 30px rgba(0, 229, 255, 0.2) inset;
            animation: pulseRing 2.5s ease-in-out infinite;
        }

        .arc-core {
            position: absolute;
            inset: 32%;
            border-radius: 50%;
            background: radial-gradient(circle at 35% 35%,
                #ffffff 0%,
                var(--glow) 15%,
                #0099cc 40%,
                #003344 70%,
                #001018 100%);
            box-shadow:
                0 0 30px var(--glow),
                0 0 60px rgba(0, 229, 255, 0.5),
                0 0 100px rgba(0, 229, 255, 0.25),
                inset 0 0 25px rgba(255, 255, 255, 0.4);
            animation: corePulse 3s ease-in-out infinite;
        }

        .arc-ticks {
            position: absolute;
            inset: -8%;
            border-radius: 50%;
        }

        .arc-tick {
            position: absolute;
            top: 50%;
            left: 50%;
            width: 2px;
            height: 8px;
            background: var(--cyan);
            transform-origin: center -180%;
            opacity: 0.5;
        }

        @keyframes spin { to { transform: rotate(360deg); } }
        @keyframes spinReverse { to { transform: rotate(-360deg); } }
        @keyframes pulseRing {
            0%, 100% { opacity: 0.6; transform: scale(1); }
            50% { opacity: 1; transform: scale(1.02); }
        }
        @keyframes corePulse {
            0%, 100% { filter: brightness(1); }
            50% { filter: brightness(1.25); }
        }

        /* Title — glow on wrapper so background-clip text does not clip glyphs (e.g. D) */
        .title-glow {
            display: inline-block;
            max-width: 100%;
            padding: 0 0.35em;
            filter: drop-shadow(0 0 20px rgba(0, 247, 255, 0.5));
            animation: titleShimmer 4s ease-in-out infinite alternate;
        }

        .title-main {
            font-family: 'Orbitron', sans-serif;
            font-weight: 800;
            line-height: 1.05;
            letter-spacing: 0.1em;
            padding-right: 0.12em;
            background: linear-gradient(180deg, #ffffff 0%, var(--glow) 45%, var(--arc) 100%);
            -webkit-background-clip: text;
            background-clip: text;
            -webkit-text-fill-color: transparent;
            color: transparent;
        }

        @keyframes titleShimmer {
            from { filter: drop-shadow(0 0 15px rgba(0, 247, 255, 0.4)); }
            to { filter: drop-shadow(0 0 35px rgba(0, 247, 255, 0.8)); }
        }

        /* Live status dot */
        .status-live::before {
            content: '';
            display: inline-block;
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: var(--green);
            box-shadow: 0 0 8px var(--green), 0 0 16px var(--green);
            animation: blink 1.2s ease-in-out infinite;
            margin-right: 8px;
            vertical-align: middle;
        }

        @keyframes blink {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.5; transform: scale(0.85); }
        }

        /* Voice bars */
        .voice-bar {
            width: 3px;
            background: linear-gradient(180deg, var(--glow), transparent);
            border-radius: 2px;
            animation: voiceWave 1.2s ease-in-out infinite;
        }

        @keyframes voiceWave {
            0%, 100% { height: 8px; opacity: 0.4; }
            50% { height: 28px; opacity: 1; }
        }

        /* Terminal */
        .terminal-wrap {
            background: rgba(0, 8, 16, 0.75);
            border: 1px solid rgba(0, 229, 255, 0.2);
            font-family: 'Share Tech Mono', monospace;
        }

        .terminal-wrap::after {
            content: '';
            position: absolute;
            inset: 0;
            background: repeating-linear-gradient(
                0deg,
                transparent,
                transparent 2px,
                rgba(0, 229, 255, 0.03) 2px,
                rgba(0, 229, 255, 0.03) 4px
            );
            pointer-events: none;
        }

        .terminal-line {
            opacity: 0;
            transform: translateX(-8px);
            animation: termIn 0.5s forwards;
        }

        @keyframes termIn {
            to { opacity: 1; transform: translateX(0); }
        }

        .cursor-blink::after {
            content: '▋';
            color: var(--glow);
            animation: cursor 1s step-end infinite;
            margin-left: 2px;
        }

        @keyframes cursor {
            50% { opacity: 0; }
        }

        /* Metric ring */
        .metric-ring svg {
            transform: rotate(-90deg);
        }

        .metric-ring circle {
            fill: none;
            stroke-width: 3;
        }

        .metric-bg { stroke: rgba(0, 229, 255, 0.12); }
        .metric-fg {
            stroke: var(--glow);
            stroke-linecap: round;
            stroke-dasharray: 100;
            stroke-dashoffset: 100;
            animation: fillRing 2s ease forwards;
            filter: drop-shadow(0 0 4px var(--glow));
        }

        @keyframes fillRing {
            to { stroke-dashoffset: var(--offset, 20); }
        }

        /* Radar */
        .radar {
            position: relative;
            border-radius: 50%;
            border: 1px solid rgba(0, 229, 255, 0.25);
            overflow: hidden;
        }

        .radar-sweep {
            position: absolute;
            inset: 0;
            background: conic-gradient(from 0deg, transparent 0deg, rgba(0, 247, 255, 0.35) 30deg, transparent 60deg);
            animation: radarSpin 4s linear infinite;
        }

        .radar-grid {
            position: absolute;
            inset: 0;
            background:
                radial-gradient(circle, transparent 30%, rgba(0, 229, 255, 0.08) 31%, transparent 32%),
                radial-gradient(circle, transparent 60%, rgba(0, 229, 255, 0.06) 61%, transparent 62%),
                linear-gradient(0deg, transparent 49.5%, rgba(0, 229, 255, 0.15) 50%, transparent 50.5%),
                linear-gradient(90deg, transparent 49.5%, rgba(0, 229, 255, 0.15) 50%, transparent 50.5%);
        }

        @keyframes radarSpin {
            to { transform: rotate(360deg); }
        }

        /* Card hover */
        .sys-card {
            transition: transform 0.35s ease, box-shadow 0.35s ease, border-color 0.35s ease;
        }

        .sys-card:hover {
            transform: translateY(-4px);
            border-color: rgba(0, 247, 255, 0.45);
            box-shadow: 0 0 25px rgba(0, 229, 255, 0.15);
        }

        /* Particle canvas */
        #particleCanvas {
            position: fixed;
            inset: 0;
            z-index: 1;
            pointer-events: none;
            opacity: 0.5;
        }

        .content-layer {
            position: relative;
            z-index: 10;
        }

        /* Reduce motion */
        @media (prefers-reduced-motion: reduce) {
            *, *::before, *::after {
                animation-duration: 0.01ms !important;
                animation-iteration-count: 1 !important;
            }
        }
    </style>
</head>
<body class="antialiased">

    <canvas id="particleCanvas" aria-hidden="true"></canvas>

    <div class="bg-layer bg-radial"></div>
    <div class="bg-layer hex-grid"></div>
    <div class="bg-layer"><div class="scan-line"></div></div>

    <div class="content-layer min-h-screen flex flex-col">

        <!-- Top bar -->
        <header class="w-full px-4 sm:px-6 lg:px-10 py-4 sm:py-5 flex flex-wrap items-center justify-between gap-3 border-b border-cyan-500/10">
            <div class="flex items-center gap-3 sm:gap-4">
                <div class="flex gap-1.5" aria-hidden="true">
                    <span class="w-3 h-3 rounded-full bg-red-500/90 shadow-[0_0_8px_#ff3d5a]"></span>
                    <span class="w-3 h-3 rounded-full bg-amber-400/90 shadow-[0_0_8px_#ffb300]"></span>
                    <span class="w-3 h-3 rounded-full bg-emerald-400/90 shadow-[0_0_8px_#00ff9d]"></span>
                </div>
                <div class="font-mono text-xs sm:text-sm tracking-[0.25em] text-cyan-400/80 uppercase">
                    J.A.R.V.I.S <span class="text-cyan-300/40 hidden sm:inline">//</span>
                    <span class="text-cyan-300/60 hidden sm:inline"> Porter Protocol</span>
                </div>
            </div>

            <div class="flex flex-wrap items-center gap-4 sm:gap-8">
                <div class="flex items-end gap-0.5 h-7" aria-hidden="true">
                    <div class="voice-bar" style="animation-delay:0s"></div>
                    <div class="voice-bar" style="animation-delay:0.15s"></div>
                    <div class="voice-bar" style="animation-delay:0.3s"></div>
                    <div class="voice-bar" style="animation-delay:0.1s"></div>
                    <div class="voice-bar" style="animation-delay:0.25s"></div>
                    <div class="voice-bar" style="animation-delay:0.05s"></div>
                    <div class="voice-bar" style="animation-delay:0.2s"></div>
                </div>
                <div class="status-live font-orbitron text-xs sm:text-sm font-semibold tracking-[0.2em] text-emerald-400 uppercase">
                    System Live
                </div>
                <time id="liveClock" class="font-mono text-sm sm:text-base text-cyan-300 tabular-nums tracking-wider"></time>
            </div>
        </header>

        <!-- Main -->
        <main class="flex-1 w-full max-w-[1400px] mx-auto px-4 sm:px-6 lg:px-10 py-6 sm:py-10 lg:py-12">

            <div class="grid grid-cols-1 lg:grid-cols-12 gap-5 lg:gap-6">

                <!-- Left panel — desktop -->
                <aside class="hidden lg:flex lg:col-span-3 flex-col gap-4">
                    <div class="hud-frame rounded-2xl p-5 flex-1">
                        <div class="corner-bracket tl"></div>
                        <div class="corner-bracket br"></div>
                        <p class="font-orbitron text-[10px] tracking-[0.3em] text-cyan-500/70 mb-4">DIAGNOSTICS</p>
                        <div class="radar w-full aspect-square max-w-[180px] mx-auto mb-5">
                            <div class="radar-grid"></div>
                            <div class="radar-sweep"></div>
                        </div>
                        <ul class="space-y-3 font-mono text-xs sm:text-sm">
                            <li class="flex justify-between border-b border-cyan-500/10 pb-2">
                                <span class="text-cyan-400/60">NODE</span>
                                <span class="text-cyan-200">porter-api-01</span>
                            </li>
                            <li class="flex justify-between border-b border-cyan-500/10 pb-2">
                                <span class="text-cyan-400/60">REGION</span>
                                <span class="text-cyan-200" id="regionTag">—</span>
                            </li>
                            <li class="flex justify-between border-b border-cyan-500/10 pb-2">
                                <span class="text-cyan-400/60">UPTIME</span>
                                <span class="text-emerald-400 tabular-nums" id="uptime">00:00:00</span>
                            </li>
                            <li class="flex justify-between">
                                <span class="text-cyan-400/60">LATENCY</span>
                                <span class="text-cyan-200 tabular-nums"><span id="latency">12</span> ms</span>
                            </li>
                        </ul>
                    </div>

                    <div class="hud-frame rounded-2xl p-5">
                        <p class="font-orbitron text-[10px] tracking-[0.3em] text-cyan-500/70 mb-3">CORE LOAD</p>
                        <div class="flex justify-around gap-2">
                            <div class="metric-ring text-center">
                                <svg width="64" height="64" viewBox="0 0 36 36">
                                    <circle class="metric-bg" cx="18" cy="18" r="15.9"/>
                                    <circle class="metric-fg" cx="18" cy="18" r="15.9" style="--offset:18" id="ringCpu"/>
                                </svg>
                                <p class="font-mono text-[10px] mt-1 text-cyan-400/70">CPU</p>
                                <p class="font-orbitron text-sm text-cyan-200" id="cpuVal">—</p>
                            </div>
                            <div class="metric-ring text-center">
                                <svg width="64" height="64" viewBox="0 0 36 36">
                                    <circle class="metric-bg" cx="18" cy="18" r="15.9"/>
                                    <circle class="metric-fg" cx="18" cy="18" r="15.9" style="--offset:28" id="ringMem"/>
                                </svg>
                                <p class="font-mono text-[10px] mt-1 text-cyan-400/70">MEM</p>
                                <p class="font-orbitron text-sm text-cyan-200" id="memVal">—</p>
                            </div>
                        </div>
                    </div>
                </aside>

                <!-- Center hero -->
                <section class="lg:col-span-6 flex flex-col items-center">
                    <div class="hud-frame rounded-3xl w-full p-6 sm:p-10 lg:p-12 text-center relative overflow-visible">
                        <div class="corner-bracket tl"></div>
                        <div class="corner-bracket tr"></div>
                        <div class="corner-bracket bl"></div>
                        <div class="corner-bracket br"></div>

                        <p class="font-orbitron text-[10px] sm:text-xs tracking-[0.4em] text-cyan-500/80 mb-6 sm:mb-8 uppercase">
                            Just A Rather Very Intelligent System
                        </p>

                        <div class="arc-reactor mx-auto mb-8 sm:mb-10" role="img" aria-label="Arc reactor core">
                            <div class="arc-ticks" id="arcTicks"></div>
                            <div class="arc-ring arc-ring-1"></div>
                            <div class="arc-ring arc-ring-2"></div>
                            <div class="arc-ring arc-ring-3"></div>
                            <div class="arc-core"></div>
                        </div>

                        <div class="title-glow">
                            <h1 class="title-main text-4xl sm:text-5xl md:text-6xl lg:text-7xl xl:text-8xl uppercase break-words">
                                Porter<br>Backend
                            </h1>
                        </div>

                        <p class="mt-4 sm:mt-6 font-rajdhani text-base sm:text-lg md:text-xl font-light tracking-[0.35em] text-cyan-300/80 uppercase">
                            AI-Powered Railway Infrastructure
                        </p>

                        <div class="mt-6 sm:mt-8 inline-flex items-center gap-3 px-4 py-2 rounded-full border border-emerald-500/30 bg-emerald-500/5">
                            <span class="status-live font-orbitron text-xs sm:text-sm tracking-[0.25em] text-emerald-400">Operational</span>
                            <span class="text-cyan-500/40">|</span>
                            <span class="font-mono text-xs sm:text-sm text-cyan-300/90" id="liveStatusText">All systems nominal</span>
                        </div>

                        <!-- Mobile metrics row -->
                        <div class="lg:hidden mt-8 grid grid-cols-3 gap-3 text-center">
                            <div class="rounded-xl border border-cyan-500/15 bg-black/30 py-3 px-2">
                                <p class="font-mono text-[10px] text-cyan-500/60 uppercase">Uptime</p>
                                <p class="font-orbitron text-sm text-emerald-400 tabular-nums mt-1" id="uptimeMobile">00:00:00</p>
                            </div>
                            <div class="rounded-xl border border-cyan-500/15 bg-black/30 py-3 px-2">
                                <p class="font-mono text-[10px] text-cyan-500/60 uppercase">Latency</p>
                                <p class="font-orbitron text-sm text-cyan-200 tabular-nums mt-1"><span id="latencyMobile">12</span>ms</p>
                            </div>
                            <div class="rounded-xl border border-cyan-500/15 bg-black/30 py-3 px-2">
                                <p class="font-mono text-[10px] text-cyan-500/60 uppercase">Health</p>
                                <p class="font-orbitron text-sm text-emerald-400 mt-1">100%</p>
                            </div>
                        </div>
                    </div>

                    <!-- Terminal -->
                    <div class="terminal-wrap relative rounded-2xl mt-5 sm:mt-6 p-4 sm:p-6 w-full overflow-hidden">
                        <div class="flex items-center gap-2 mb-4 pb-3 border-b border-cyan-500/15">
                            <span class="font-orbitron text-[10px] tracking-[0.2em] text-cyan-500/70">CONSOLE</span>
                            <span class="flex-1"></span>
                            <span class="font-mono text-[10px] text-cyan-500/50" id="termSession">session-7f3a</span>
                        </div>
                        <div id="terminal" class="text-left text-xs sm:text-sm space-y-2 min-h-[120px] sm:min-h-[140px] text-cyan-200/90">
                            <div class="terminal-line cursor-blink" style="animation-delay:0.2s">&gt; Awaiting input...</div>
                        </div>
                    </div>
                </section>

                <!-- Right panel — desktop -->
                <aside class="hidden lg:flex lg:col-span-3 flex-col gap-4">
                    <div class="hud-frame rounded-2xl p-5">
                        <p class="font-orbitron text-[10px] tracking-[0.3em] text-cyan-500/70 mb-4">SERVICES</p>
                        <ul class="space-y-3" id="serviceList">
                            <li class="flex items-center justify-between text-sm font-mono">
                                <span class="text-cyan-300/80">REST API</span>
                                <span class="text-emerald-400 text-xs tracking-wider">● LIVE</span>
                            </li>
                            <li class="flex items-center justify-between text-sm font-mono">
                                <span class="text-cyan-300/80">PostgreSQL</span>
                                <span class="text-emerald-400 text-xs tracking-wider">● SYNCED</span>
                            </li>
                            <li class="flex items-center justify-between text-sm font-mono">
                                <span class="text-cyan-300/80">Auth / OTP</span>
                                <span class="text-emerald-400 text-xs tracking-wider">● ACTIVE</span>
                            </li>
                            <li class="flex items-center justify-between text-sm font-mono">
                                <span class="text-cyan-300/80">Train Data</span>
                                <span class="text-emerald-400 text-xs tracking-wider">● ONLINE</span>
                            </li>
                        </ul>
                    </div>

                    <div class="hud-frame rounded-2xl p-5 flex-1">
                        <p class="font-orbitron text-[10px] tracking-[0.3em] text-cyan-500/70 mb-4">STACK</p>
                        <div class="space-y-4 font-mono text-sm">
                            <div>
                                <div class="flex justify-between mb-1">
                                    <span class="text-cyan-400/60">Django</span>
                                    <span class="text-cyan-200">5.x</span>
                                </div>
                                <div class="h-1 rounded-full bg-cyan-900/40 overflow-hidden">
                                    <div class="h-full bg-gradient-to-r from-cyan-500 to-emerald-400 rounded-full w-[92%] animate-pulse"></div>
                                </div>
                            </div>
                            <div>
                                <div class="flex justify-between mb-1">
                                    <span class="text-cyan-400/60">DRF</span>
                                    <span class="text-cyan-200">API</span>
                                </div>
                                <div class="h-1 rounded-full bg-cyan-900/40 overflow-hidden">
                                    <div class="h-full bg-gradient-to-r from-cyan-500 to-blue-400 rounded-full w-[88%]"></div>
                                </div>
                            </div>
                            <div>
                                <div class="flex justify-between mb-1">
                                    <span class="text-cyan-400/60">Render</span>
                                    <span class="text-cyan-200">Cloud</span>
                                </div>
                                <div class="h-1 rounded-full bg-cyan-900/40 overflow-hidden">
                                    <div class="h-full bg-gradient-to-r from-cyan-500 to-cyan-300 rounded-full w-[100%]"></div>
                                </div>
                            </div>
                        </div>
                        <p class="mt-6 font-rajdhani text-xs text-cyan-500/50 tracking-widest uppercase text-center">
                            Secure · Scalable · Intelligent
                        </p>
                    </div>
                </aside>
            </div>

            <!-- System cards -->
            <div class="mt-6 sm:mt-10 grid grid-cols-2 md:grid-cols-4 gap-3 sm:gap-4">
                <div class="sys-card hud-frame rounded-xl p-4 sm:p-5 text-center">
                    <p class="font-orbitron text-[9px] sm:text-[10px] tracking-[0.25em] text-cyan-500/70 mb-2">FRAMEWORK</p>
                    <p class="font-rajdhani text-lg sm:text-xl font-semibold text-white">Django + DRF</p>
                </div>
                <div class="sys-card hud-frame rounded-xl p-4 sm:p-5 text-center">
                    <p class="font-orbitron text-[9px] sm:text-[10px] tracking-[0.25em] text-cyan-500/70 mb-2">SERVER</p>
                    <p class="font-rajdhani text-lg sm:text-xl font-semibold text-white">Render Cloud</p>
                </div>
                <div class="sys-card hud-frame rounded-xl p-4 sm:p-5 text-center">
                    <p class="font-orbitron text-[9px] sm:text-[10px] tracking-[0.25em] text-cyan-500/70 mb-2">DATABASE</p>
                    <p class="font-rajdhani text-lg sm:text-xl font-semibold text-white">PostgreSQL</p>
                </div>
                <div class="sys-card hud-frame rounded-xl p-4 sm:p-5 text-center col-span-2 md:col-span-1">
                    <p class="font-orbitron text-[9px] sm:text-[10px] tracking-[0.25em] text-cyan-500/70 mb-2">STATUS</p>
                    <p class="font-orbitron text-lg sm:text-xl font-bold text-emerald-400 tracking-wider status-live">LIVE</p>
                </div>
            </div>
        </main>

        <footer class="px-4 sm:px-6 py-4 border-t border-cyan-500/10 text-center">
            <p class="font-mono text-[10px] sm:text-xs text-cyan-500/40 tracking-[0.2em]">
                PORTER CONNECT © <span id="year"></span> — STARK-LEVEL BACKEND INTERFACE
            </p>
        </footer>
    </div>

    <script>
    (function () {
        const bootLines = [
            '> Initializing Porter Backend core...',
            '> Loading JARVIS security protocols...',
            '> Connecting Render cloud infrastructure...',
            '> PostgreSQL cluster synchronized.',
            '> Django REST framework online.',
            '> OTP & authentication modules active.',
            '> Train & station data feeds connected.',
            '> System status: LIVE — All systems nominal.',
        ];

        const statusPhrases = [
            'All systems nominal',
            'Neural link stable',
            'Cloud sync optimal',
            'API gateway secure',
            'Database replication OK',
        ];

        let bootIndex = 0;
        let startTime = Date.now();

        // Arc ticks
        const ticksEl = document.getElementById('arcTicks');
        if (ticksEl) {
            for (let i = 0; i < 24; i++) {
                const t = document.createElement('div');
                t.className = 'arc-tick';
                t.style.transform = 'rotate(' + (i * 15) + 'deg) translateY(-90px)';
                ticksEl.appendChild(t);
            }
        }

        // Clock
        function updateClock() {
            const now = new Date();
            const el = document.getElementById('liveClock');
            if (el) {
                el.textContent = now.toLocaleTimeString('en-GB', { hour12: false }) + ' UTC';
            }
        }

        // Uptime
        function updateUptime() {
            const s = Math.floor((Date.now() - startTime) / 1000);
            const h = String(Math.floor(s / 3600)).padStart(2, '0');
            const m = String(Math.floor((s % 3600) / 60)).padStart(2, '0');
            const sec = String(s % 60).padStart(2, '0');
            const str = h + ':' + m + ':' + sec;
            ['uptime', 'uptimeMobile'].forEach(id => {
                const el = document.getElementById(id);
                if (el) el.textContent = str;
            });
        }

        // Metrics
        function updateMetrics() {
            const cpu = 18 + Math.floor(Math.random() * 22);
            const mem = 42 + Math.floor(Math.random() * 18);
            const lat = 8 + Math.floor(Math.random() * 14);
            const cpuEl = document.getElementById('cpuVal');
            const memEl = document.getElementById('memVal');
            const latEl = document.getElementById('latency');
            const latMob = document.getElementById('latencyMobile');
            if (cpuEl) cpuEl.textContent = cpu + '%';
            if (memEl) memEl.textContent = mem + '%';
            if (latEl) latEl.textContent = lat;
            if (latMob) latMob.textContent = lat;
            const ringCpu = document.getElementById('ringCpu');
            const ringMem = document.getElementById('ringMem');
            if (ringCpu) ringCpu.style.setProperty('--offset', 100 - cpu);
            if (ringMem) ringMem.style.setProperty('--offset', 100 - mem);
        }

        // Terminal boot
        const terminal = document.getElementById('terminal');
        function addLine(text, delay) {
            setTimeout(() => {
                if (!terminal) return;
                const line = document.createElement('div');
                line.className = 'terminal-line';
                line.textContent = text;
                line.style.animationDelay = '0s';
                terminal.querySelector('.cursor-blink')?.classList.remove('cursor-blink');
                terminal.appendChild(line);
                if (bootIndex < bootLines.length) {
                    const next = document.createElement('div');
                    next.className = 'terminal-line cursor-blink';
                    next.textContent = '> ';
                    terminal.appendChild(next);
                }
                terminal.scrollTop = terminal.scrollHeight;
            }, delay);
        }

        bootLines.forEach((line, i) => addLine(line, 400 + i * 700));
        bootIndex = bootLines.length;

        // Live status text rotation
        let statusIdx = 0;
        setInterval(() => {
            statusIdx = (statusIdx + 1) % statusPhrases.length;
            const el = document.getElementById('liveStatusText');
            if (el) el.textContent = statusPhrases[statusIdx];
        }, 4000);

        // Region from TZ
        const regionEl = document.getElementById('regionTag');
        if (regionEl) {
            try {
                regionEl.textContent = Intl.DateTimeFormat().resolvedOptions().timeZone.split('/').pop() || 'GLOBAL';
            } catch (_) {
                regionEl.textContent = 'GLOBAL';
            }
        }

        document.getElementById('year').textContent = new Date().getFullYear();

        const sessionEl = document.getElementById('termSession');
        if (sessionEl) {
            sessionEl.textContent = 'session-' + Math.random().toString(16).slice(2, 6);
        }

        updateClock();
        updateUptime();
        updateMetrics();
        setInterval(updateClock, 1000);
        setInterval(updateUptime, 1000);
        setInterval(updateMetrics, 3000);

        // Particle network
        const canvas = document.getElementById('particleCanvas');
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        let particles = [];
        const PARTICLE_COUNT = window.innerWidth < 640 ? 35 : 70;

        function resize() {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        }

        function initParticles() {
            particles = [];
            for (let i = 0; i < PARTICLE_COUNT; i++) {
                particles.push({
                    x: Math.random() * canvas.width,
                    y: Math.random() * canvas.height,
                    vx: (Math.random() - 0.5) * 0.4,
                    vy: (Math.random() - 0.5) * 0.4,
                });
            }
        }

        function drawParticles() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            const maxDist = window.innerWidth < 768 ? 100 : 140;
            for (let i = 0; i < particles.length; i++) {
                const p = particles[i];
                p.x += p.vx;
                p.y += p.vy;
                if (p.x < 0 || p.x > canvas.width) p.vx *= -1;
                if (p.y < 0 || p.y > canvas.height) p.vy *= -1;
                ctx.beginPath();
                ctx.arc(p.x, p.y, 1.2, 0, Math.PI * 2);
                ctx.fillStyle = 'rgba(0, 229, 255, 0.6)';
                ctx.fill();
                for (let j = i + 1; j < particles.length; j++) {
                    const q = particles[j];
                    const dx = p.x - q.x;
                    const dy = p.y - q.y;
                    const d = Math.sqrt(dx * dx + dy * dy);
                    if (d < maxDist) {
                        ctx.beginPath();
                        ctx.strokeStyle = 'rgba(0, 229, 255, ' + (0.15 * (1 - d / maxDist)) + ')';
                        ctx.lineWidth = 0.5;
                        ctx.moveTo(p.x, p.y);
                        ctx.lineTo(q.x, q.y);
                        ctx.stroke();
                    }
                }
            }
            requestAnimationFrame(drawParticles);
        }

        resize();
        initParticles();
        window.addEventListener('resize', () => { resize(); initParticles(); });
        drawParticles();
    })();
    </script>
</body>
</html>
    """)
