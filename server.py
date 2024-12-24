from flask import Flask, Response
import time

app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def analyze():
    def workflow():
        yield "data: Collecting data...\n\n"
        time.sleep(2)
        yield "data: Processing data...\n\n"
        time.sleep(2)
        yield "data: Finalizing...\n\n"
        time.sleep(1)
        yield "data: Completed!\n\n"
    return Response(workflow(), content_type='text/event-stream')

if __name__ == '__main__':
    app.run(debug=True)
