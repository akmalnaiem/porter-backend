from django.http import HttpResponse


def home(request):
    return HttpResponse("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Porter Backend</title>

        <style>
            body{
                margin:0;
                height:100vh;
                display:flex;
                justify-content:center;
                align-items:center;
                background:#0f172a;
                font-family:Arial, sans-serif;
                overflow:hidden;
            }

            .card{
                padding:40px 60px;
                border-radius:20px;
                background:#111827;
                color:white;
                text-align:center;
                box-shadow:0 0 20px #00ffcc;
                animation: glow 2s infinite alternate;
            }

            h1{
                font-size:40px;
                margin-bottom:10px;
            }

            p{
                color:#9ca3af;
                font-size:18px;
            }

            .dot{
                display:inline-block;
                width:12px;
                height:12px;
                background:#00ff66;
                border-radius:50%;
                margin-right:8px;
                animation: pulse 1s infinite;
            }

            @keyframes glow{
                from{
                    box-shadow:0 0 10px #00ffcc;
                }
                to{
                    box-shadow:0 0 35px #00ffcc;
                }
            }

            @keyframes pulse{
                0%{
                    transform:scale(1);
                    opacity:1;
                }
                50%{
                    transform:scale(1.5);
                    opacity:0.5;
                }
                100%{
                    transform:scale(1);
                    opacity:1;
                }
            }
        </style>
    </head>

    <body>

        <div class="card">
            <h1>🚀 Porter Backend</h1>

            <p>
                <span class="dot"></span>
                Server Status : LIVE
            </p>

            <p>Running on Render Cloud ☁️</p>
        </div>

    </body>
    </html>
    """)
