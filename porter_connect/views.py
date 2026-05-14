from django.http import HttpResponse


def home(request):
    return HttpResponse("""
    <!DOCTYPE html>
    <html>

    <head>
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
                background:linear-gradient(-45deg,#000000,#0f172a,#001f3f,#000000);
                background-size:400% 400%;
                animation:bg 10s ease infinite;
                font-family:Arial,sans-serif;
            }

            .container{
                position:relative;
                text-align:center;
                z-index:2;
            }

            h1{
                color:white;
                font-size:70px;
                text-transform:uppercase;
                letter-spacing:4px;

                border-right:4px solid #00ffff;
                width:0;
                overflow:hidden;
                white-space:nowrap;

                animation:
                    typing 3s steps(20,end) forwards,
                    blink .8s infinite,
                    glow 2s infinite alternate;
            }

            p{
                margin-top:20px;
                color:#00ffff;
                font-size:22px;
                opacity:0;
                animation:fadeIn 2s ease forwards;
                animation-delay:3s;
            }

            .circle{
                position:absolute;
                border-radius:50%;
                background:rgba(0,255,255,0.15);
                animation:float 10s linear infinite;
            }

            .circle:nth-child(1){
                width:120px;
                height:120px;
                left:10%;
                animation-duration:8s;
            }

            .circle:nth-child(2){
                width:200px;
                height:200px;
                right:15%;
                animation-duration:12s;
            }

            .circle:nth-child(3){
                width:80px;
                height:80px;
                bottom:10%;
                left:40%;
                animation-duration:6s;
            }

            @keyframes typing{
                from{
                    width:0;
                }

                to{
                    width:100%;
                }
            }

            @keyframes blink{
                50%{
                    border-color:transparent;
                }
            }

            @keyframes glow{
                from{
                    text-shadow:0 0 10px #00ffff;
                }

                to{
                    text-shadow:
                        0 0 20px #00ffff,
                        0 0 40px #00ffff,
                        0 0 60px #00ffff;
                }
            }

            @keyframes fadeIn{
                to{
                    opacity:1;
                }
            }

            @keyframes bg{
                0%{
                    background-position:0% 50%;
                }

                50%{
                    background-position:100% 50%;
                }

                100%{
                    background-position:0% 50%;
                }
            }

            @keyframes float{
                0%{
                    transform:translateY(100vh) scale(0);
                }

                100%{
                    transform:translateY(-120vh) scale(1.5);
                }
            }
        </style>
    </head>

    <body>

        <div class="circle"></div>
        <div class="circle"></div>
        <div class="circle"></div>

        <div class="container">
            <h1>Porter Backend</h1>
            <p>● SERVER STATUS : LIVE</p>
        </div>
    </body>
    </html>
    """)
