from coordinator.orchestrator import JobHuntOrchestrator


def main():
    orchestrator = JobHuntOrchestrator()

    print("AI Fresher Job Hunt Agent")
    print("-" * 40)

    print("\nPipeline:")

    for agent in orchestrator.get_pipeline():
        print(f"• {agent.name}")

    print("\nBackend initialized successfully.")


if __name__ == "__main__":
    main()
