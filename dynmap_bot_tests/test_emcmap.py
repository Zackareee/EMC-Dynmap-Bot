from emcmap import parser


def test_default_output(monkeypatch):
    """Test default output filename when no -o argument is provided"""
    monkeypatch.setattr("sys.argv", ["emcmap.py", "-t", "town1"])
    args = parser.parse_args()
    assert args.output == "out.png"
    assert args.towns == ["town1"]
    assert args.uncropped is False


def test_custom_output(monkeypatch):
    """Test specifying an output filename"""
    monkeypatch.setattr("sys.argv", ["render.py", "-t", "town1", "-o", "map.jpg"])
    args = parser.parse_args()
    assert args.output == "map.jpg"
    assert args.towns == ["town1"]


def test_nations(monkeypatch):
    """Test downloading nations instead of towns"""
    monkeypatch.setattr("sys.argv", ["render.py", "-n", "nationA", "nationB"])
    args = parser.parse_args()
    assert args.nations == ["nationA", "nationB"]
    assert args.towns is None


def test_uncropped_flag(monkeypatch):
    """Test if -uc flag enables uncropped mode"""
    monkeypatch.setattr("sys.argv", ["render.py", "-t", "town1", "-uc"])
    args = parser.parse_args()
    assert args.uncropped is True
