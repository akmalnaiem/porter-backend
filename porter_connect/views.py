from django.http import HttpResponse


def home(request):
    return HttpResponse("""
    <html>
        <head>
            <title>Porter Backend</title>

            <style>
                body{
                    background:black;
                    color:white;
                    display:flex;
                    justify-content:center;
                    align-items:center;
                    height:100vh;
                    font-family:Arial;
                }

                h1{
                    animation: glow 1s infinite alternate;
                }

                @keyframes glow{
                    from{
                        opacity:0.5;
                    }

                    to{
                        opacity:1;
                    }
                }
            </style>
        </head>

        <body>
            <h1>Porter Backend LIVE</h1>
        </body>
    </html>
    """)