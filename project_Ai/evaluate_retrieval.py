from evaluation_cases import RETRIEVAL_CASES
from vector_search import search_similar_document


def evaluate_retrieval():
    passed_cases = 0
    total_cases = len(RETRIEVAL_CASES)

    for case in RETRIEVAL_CASES:
        question = case["question"]
        expected_title = case["expected_title"]

        result = search_similar_document(question)

        if result is None:
            actual_title = None
            similarity = None
        else:
            actual_title = result["title"]
            similarity = round(float(result["similarity"]), 3)

        passed = actual_title == expected_title

        if passed:
            passed_cases += 1

        print(f"Question: {question}")
        print(f"Expected Title: {expected_title}")
        print(f"Actual Title: {actual_title}")
        print(f"Similarity: {similarity}")
        print(f"Passed: {passed}")
        print(f"Result: {'PASS' if passed else 'FAIL'}")

    accuracy = passed_cases / total_cases

    print("\nEvaluation summary")
    print("------------------")
    print("Passed:", passed_cases)
    print("Total:", total_cases)
    print("Accuracy:", f"{accuracy:.1%}")


if __name__ == "__main__":
    evaluate_retrieval()
