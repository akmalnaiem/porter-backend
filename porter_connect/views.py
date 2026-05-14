from django.http import HttpResponse


def home(request):
    return HttpResponse("""
    <!DOCTYPE html>
    <html lang="en">

    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">

        <title>Porter Backend</title>

        <style>

            *{
                margin:0;
                padding:0;
                box-sizing:border-box;
            }

            body{
                height:100vh;
                overflow:hidden;
                display:flex;
                justify-content:center;
                align-items:center;
                background:black;
                font-family:Arial,sans-serif;
                position:relative;
            }

            /* Animated Grid Background */

            body::before{
                content:"";
                position:absolute;
                width:200%;
                height:200%;

                background-image:
                    linear-gradient(rgba(0,255,255,0.08) 1px, transparent 1px),
                    linear-gradient(90deg, rgba(0,255,255,0.08) 1px, transparent 1px);

                background-size:50px 50px;

                transform:perspective(500px) rotateX(75deg);

                animation:gridMove 8s linear infinite;
            }

            /* Floating Stars */

            .star{
                position:absolute;
                width:2px;
                height:2px;
                background:white;
                border-radius:50%;

                animation:starMove linear infinite;
            }

            /* Main Glass Card */

            .container{
                position:relative;
                z-index:10;

                padding:60px;
                border-radius:30px;

                background:rgba(255,255,255,0.05);

                backdrop-filter:blur(12px);

                border:1px solid rgba(255,255,255,0.1);

                box-shadow:
                    0 0 20px rgba(0,255,255,0.3),
                    0 0 60px rgba(0,255,255,0.2);

                text-align:center;

                animation:floatCard 4s ease-in-out infinite;
            }

            /* Rotating Ring */

            .container::before{
                content:"";
                position:absolute;

                top:-10px;
                left:-10px;
                right:-10px;
                bottom:-10px;

                border-radius:40px;

                border:2px solid transparent;
                border-top:2px solid cyan;
                border-bottom:2px solid #00ff99;

                animation:rotate 4s linear infinite;
            }

            /* Main Heading */

            h1{
                font-size:75px;
                color:white;

                text-transform:uppercase;
                letter-spacing:6px;

                position:relative;

                text-shadow:
                    0 0 10px cyan,
                    0 0 20px cyan,
                    0 0 40px cyan;

                animation:textPulse 2s infinite alternate;
            }

            /* Scanline */

            h1::after{
                content:"";
                position:absolute;

                left:0;
                top:0;

                width:100%;
                height:100%;

                background:linear-gradient(
                    transparent,
                    rgba(255,255,255,0.2),
                    transparent
                );

                animation:scan 3s linear infinite;
            }

            /* Status Text */

            p{
                margin-top:25px;

                color:#00ffff;
                font-size:24px;
                letter-spacing:3px;

                animation:fadeIn 3s ease forwards;
            }

            /* Live Dot */

            .dot{
                display:inline-block;

                width:14px;
                height:14px;

                background:#00ff66;

                border-radius:50%;
                margin-right:10px;

                box-shadow:
                    0 0 10px #00ff66,
                    0 0 20px #00ff66;

                animation:pulse 1s infinite;
            }

            /* Animations */

            @keyframes rotate{
                100%{
                    transform:rotate(360deg);
                }
            }

            @keyframes pulse{
                50%{
                    transform:scale(1.5);
                }
            }

            @keyframes fadeIn{
                from{
                    opacity:0;
                    transform:translateY(20px);
                }

                to{
                    opacity:1;
                    transform:translateY(0);
                }
            }

            @keyframes textPulse{
                from{
                    text-shadow:
                        0 0 10px cyan,
                        0 0 20px cyan;
                }

                to{
                    text-shadow:
                        0 0 20px cyan,
                        0 0 40px cyan,
                        0 0 80px cyan;
                }
            }

            @keyframes scan{
                0%{
                    transform:translateY(-100%);
                }

                100%{
                    transform:translateY(100%);
                }
            }

            @keyframes gridMove{
                0%{
                    transform:
                        perspective(500px)
                        rotateX(75deg)
                        translateY(0);
                }

                100%{
                    transform:
                        perspective(500px)
                        rotateX(75deg)
                        translateY(50px);
                }
            }

            @keyframes floatCard{
                0%,100%{
                    transform:translateY(0);
                }

                50%{
                    transform:translateY(-15px);
                }
            }

            @keyframes starMove{
                from{
                    transform:translateY(100vh);
                }

                to{
                    transform:translateY(-100vh);
                }
            }

        </style>

    </head>

    <body>

        <!-- Stars -->

        <div class="star" style="left:10%; animation-duration:5s;"></div>
        <div class="star" style="left:20%; animation-duration:7s;"></div>
        <div class="star" style="left:35%; animation-duration:4s;"></div>
        <div class="star" style="left:50%; animation-duration:9s;"></div>
        <div class="star" style="left:65%; animation-duration:6s;"></div>
        <div class="star" style="left:80%; animation-duration:8s;"></div>

        <!-- Main Container -->

        <div class="container">

            <h1>Porter Backend</h1>

            <p>
                <span class="dot"></span>
                SERVER STATUS : LIVE
            </p>

        </div>

    </body>

    </html>
    """)
