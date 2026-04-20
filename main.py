
from logger_config import setup_logging
from agent.agent import run_agent

def main():
    setup_logging()
    result = run_agent()


if __name__ == "__main__":
    main()
