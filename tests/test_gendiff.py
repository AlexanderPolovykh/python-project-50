from gendiff import generate_diff

def test_plain_json_diff():
    result = generate_diff(
        'tests/fixtures/file1.json',
        'tests/fixtures/file2.json'
    )
    with open('tests/fixtures/plain_json_diff_result.txt', 'rt') as file:
        text = file.read()
    print(text)
    print(result)
    assert text == result
