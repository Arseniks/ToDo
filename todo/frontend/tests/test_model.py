from todo.frontend import model


JSON = [
    {
        "name": "Собраться в школу",
        "date": "2020-06-13",
        "done": True,
        "description": "Собрать еду и рюкзак",
        "uuid": "fe6cd177-a8da-11ea-abfc-d46d6da674b6",
    },
    {
        "name": "Сходить в магазин",
        "date": "2020-06-14",
        "done": False,
        "description": "Купить воду и сок",
        "uuid": "fe6cd178-a8da-11ea-a391-d46d6da674b6",
    },
    {
        "name": "Собраться в школу",
        "date": "2020-06-15",
        "done": True,
        "description": "Собрать еду и рюкзак",
        "uuid": "fe6cd179-a8da-11ea-af26-d46d6da674b6",
    },
]

DATA = [
    {
        "name": "Собраться в школу",
        "date": "2020-06-13",
        "done": True,
        "description": "Собрать еду и рюкзак",
        "id": "fe6cd177-a8da-11ea-abfc-d46d6da674b6",
    },
    {
        "name": "Сходить в магазин",
        "date": "2020-06-14",
        "done": False,
        "description": "Купить воду и сок",
        "id": "fe6cd178-a8da-11ea-a391-d46d6da674b6",
    },
    {
        "name": "Собраться в школу",
        "date": "2020-06-15",
        "done": True,
        "description": "Собрать еду и рюкзак",
        "id": "fe6cd179-a8da-11ea-af26-d46d6da674b6",
    },
]

SELECTED_ROWS = [0, 2]


def test_make_url():
    assert model.make_url("abc/") == "http://localhost:5001/abc/"


def test_load_data_and_selected(mocker):
    mocker.patch("requests.get")
    model.requests.get.return_value.json.return_value = JSON

    assert model.load_data_and_selected("bca") == (DATA, SELECTED_ROWS)

    model.requests.get.assert_called_once_with("http://localhost:5001/bca/")
    model.requests.get.return_value.json.assert_called_once_with()


def test_save_toggle_task(mocker):
    mocker.patch("requests.patch")

    model.save_toggle_task("fe6cd179-a8da-11ea-af26-d46d6da674b6")

    model.requests.patch.assert_called_once_with(
        "http://localhost:5001/toggle/", '{"uuid":"fe6cd179-a8da-11ea-af26-d46d6da674b6"}'
    )


def test_save_task(mocker):
    mocker.patch("requests.post")

    model.save_task("Собраться в школу", "2020-06-15", "Собрать еду и рюкзак")

    model.requests.post.assert_called_once()
    assert model.requests.post.call_args[0][0] == "http://localhost:5001/add/"
