from guard import area
import pytest


@pytest.fixture(scope='module')
def basic_area():
    return area.Area()


@pytest.fixture(scope='module')
def basic_rectangle():
    return area.Rectangle(1, 5, 2, 6)


class TestArea():
    def test_in_area(self, basic_area):
        with pytest.raises(NotImplementedError):
            basic_area.in_area(0, 0)

    def test_all_tiles(self, basic_area):
        assert basic_area.all_tiles == []


class TestRectangle():
    @pytest.mark.parametrize('x,y,in_area', [
        (0, 0, False),
        (1, 2, True),
        (2, 4, True),
        (1, 6, False),
        (4, 5, True),
        (5, 5, False),
        (4, 6, False)
        ])
    def test_in_area(self, basic_rectangle, x, y, in_area):
        assert basic_rectangle.in_area(x, y) == in_area

    def test_bounds(self, basic_rectangle):
        assert basic_rectangle.bounds() == (1, 5, 2, 6)

    def test_all_tiles(self, basic_rectangle):
        contained = [
            basic_rectangle.in_area(x, y)
            for x, y in basic_rectangle.all_tiles
            ]
        assert all(contained)


@pytest.fixture()
def entire_map(generate_world):
    map_ = generate_world(10, 10)
    map_area = area.Rectangle.entire_map(map_)
    return map_, map_area


class TestEntireMap():
    def test_in_area(self, entire_map):
        map_, map_area = entire_map

        for tile in map_.tiles:
            assert map_area.in_area(tile.position[0], tile.position[1])

    def test_bounds(self, entire_map):
        map_, map_area = entire_map
        assert map_area.bounds() == (0, map_.xdim, 0, map_.ydim)
