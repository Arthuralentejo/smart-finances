"""Tools for the categorizer agent."""

from langchain_community.tools import TavilySearchResults


def create_categorizer_tools() -> list:
    """Create tools for the categorizer agent.

    Returns:
        List of tools for the categorizer agent.
    """
    search_tool = TavilySearchResults(
        name="search_company",
        description=(
            "Search the internet for information about a company or merchant. "
            "Use this when you need to understand what a company does to categorize "
            "a transaction correctly. Input should be the company/merchant name."
        ),
        max_results=3,
    )

    return [search_tool]
