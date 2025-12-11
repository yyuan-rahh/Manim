#!/bin/bash

# Coloured output
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to check if a command exists
check_command() {
    if ! command -v "$1" &> /dev/null; then
        echo -e "${RED}Error: $1 is not installed${NC}"
        return 1
    fi
    return 0
}

# Safe deactivate function
safe_deactivate() {
    if [ -n "$VIRTUAL_ENV" ]; then
        deactivate
    fi
}

# Function to create and activate virtual environment
setup_venv() {
    local env_name=$1
    local packages=$2
    
    if [ ! -d "$env_name" ]; then
        echo -e "${YELLOW}Creating virtual environment: $env_name${NC}"
        python3 -m venv "$env_name"
    fi
    
    source "$env_name/bin/activate"
    pip install --upgrade pip

    if [ "$env_name" = "manim-gl-env" ]; then
        if [ ! -d "manim-gl-src" ]; then
            echo -e "${YELLOW}Cloning ManimGL from source...${NC}"
            git clone https://github.com/3b1b/manim.git manim-gl-src
            cd manim-gl-src
            pip install -e .
            cd ..
        else
            cd manim-gl-src
            git pull
            pip install -e .
            cd ..
        fi
    else
        pip install $packages
    fi
}

# Check Python version
python_version=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
echo -e "${GREEN}Using Python version $python_version${NC}"

# Check for basic dependencies
check_command "python3" || exit 1
check_command "pip3" || exit 1
check_command "ffmpeg" || exit 1
check_command "git" || exit 1

# Create scenes directory if it doesn't exist
mkdir -p scenes

# Menu
echo -e "${BLUE}Choose a Manim version to run your demo:${NC}"
echo
echo -e "${GREEN}1) Teacher (Manim CE)${NC}"
echo "   Modern, documented, stable scenes (2D & basic 3D)."
echo "   Download size: ~100MB"
echo "   Install time: 2-5 minutes"
echo

echo -e "${GREEN}2) Artist (ManimGL)${NC}"
echo "   3Blue1Brown Grant-style 3D visuals with smooth rotations and shaders."
echo "   Download size: ~150MB (includes source code)"
echo "   Install time: 3-7 minutes (includes git clone and build)"
echo

echo -e "${GREEN}3) Hybrid (CE + OpenGLScene)${NC}"
echo "   CE with partial OpenGL 3D support (experimental)."
echo "   Download size: ~120MB"
echo "   Install time: 3-6 minutes"
echo

echo -e "${GREEN}4) Lite (CE 2D-only)${NC}"
echo "   Fast install, limited to 2D scenes, no LaTeX or 3D."
echo "   Download size: ~50MB"
echo "   Install time: 1-3 minutes"
echo

echo -e "${GREEN}5) Sharp (CE + MacTeX)${NC}"
echo "   Beautifully rendered LaTeX in your scenes (requires MacTeX, big download)."
echo "   Download size: ~4.5GB (mostly MacTeX)"
echo "   Install time: 15-30 minutes (depends heavily on internet speed)"
echo

read -p "Enter choice (1-5): " CHOICE

# Create a basic demo scene if none exists
create_demo_scene() {
    local scene_file=$1
    local version=$2
    
    if [ ! -f "$scene_file" ]; then
        echo -e "${YELLOW}Creating demo scene: $scene_file${NC}"
        
        if [ "$version" = "manimgl" ]
        then
            cat > "$scene_file" << 'EOL'
from manimlib import *
import numpy as np

class SimpleDemo(Scene):
    def construct(self):
        # Use classic 3B1B font
        text_top = Text("Welcome to", font="CMU Serif")
        text_bottom = Text("Manim!", font="CMU Serif")
        text_group = VGroup(text_top, text_bottom).arrange(DOWN)
        
        # Create circle that fits around the text
        circle = Circle()
        circle.surround(text_group)
        circle.scale(1.2)
        circle.set_color(BLUE)
        circle.set_fill(BLUE, opacity=0.3)
        
        # Create hexagon that surrounds the circle
        hexagon = RegularPolygon(n=6)
        hexagon.surround(circle)
        hexagon.scale(1.1)
        hexagon.set_color(YELLOW)
        hexagon.set_fill(YELLOW, opacity=0.2)
        
        # Create area equations with classic font
        r = circle.get_width() / 2  # radius of circle
        circle_area = Text("Circle Area = πr²", font="CMU Serif")
        circle_area.scale(0.8)
        circle_area.set_color(BLUE)
        circle_area.to_edge(LEFT).shift(UP)
        
        hex_area = Text("Hexagon Area = 2√3 r²", font="CMU Serif")
        hex_area.scale(0.8)
        hex_area.set_color(YELLOW)
        hex_area.next_to(circle_area, DOWN, aligned_edge=LEFT)
        
        diff_area = Text("Difference ≈ 0.1 r²", font="CMU Serif")
        diff_area.scale(0.8)
        diff_area.set_color(GREEN)
        diff_area.next_to(hex_area, DOWN, aligned_edge=LEFT)
        
        # Initial animations
        self.play(
            Write(text_top),
            Write(text_bottom),
            run_time=2
        )
        
        self.play(
            ShowCreation(circle),
            Write(circle_area),
            run_time=1.5
        )
        
        self.play(
            ShowCreation(hexagon),
            Write(hex_area),
            run_time=1.5
        )
        
        # Create 6 difference regions
        difference_pieces = VGroup()
        angles = np.linspace(0, TAU, 7)[:-1]  # 6 evenly spaced angles
        colors = [RED, ORANGE, YELLOW, GREEN, BLUE_B, PURPLE]
        
        # Create an AnnularSector for each piece
        for angle, color in zip(angles, colors):
            piece = AnnularSector(
                inner_radius=circle.get_width()/2,
                outer_radius=hexagon.get_width()/2,
                angle=TAU/6,
                start_angle=angle,
                fill_opacity=0.5,
                stroke_width=0
            )
            piece.set_color(color)
            difference_pieces.add(piece)
        
        # Highlight each piece sequentially
        for i, piece in enumerate(difference_pieces):
            self.play(
                FadeIn(piece),
                run_time=0.5
            )
            if i == len(difference_pieces) - 1:
                self.play(Write(diff_area), run_time=1)
        
        # Pause to appreciate the scene
        self.wait()
        
        # Shrink and spin everything to a point
        everything = VGroup(text_group, circle, hexagon, difference_pieces)
        equations = VGroup(circle_area, hex_area, diff_area)
        
        self.play(
            everything.animate.scale(0).move_to(ORIGIN).rotate(TAU*2),
            FadeOut(equations),
            rate_func=smooth,
            run_time=2
        )
        self.wait(0.5)
EOL
        else
            cat > "$scene_file" << 'EOL'
from manim import *

class SimpleDemo(Scene):
    def construct(self):
        circle = Circle()
        circle.set_fill(BLUE, opacity=0.5)
        self.play(Create(circle))
        
        square = Square()
        square.next_to(circle, RIGHT)
        self.play(Create(square))
        
        text = Text("Manim Demo")
        text.next_to(VGroup(circle, square), UP)
        self.play(Write(text))
        self.wait()
EOL
        fi
    fi
}

case "$CHOICE" in
  1)
    echo -e "${YELLOW}Setting up Teacher (Manim CE)...${NC}"
    setup_venv "manim-ce-env" "manim"
    create_demo_scene "scenes/demo_ce.py" "ce"
    manim scenes/demo_ce.py SimpleDemo -pql
    safe_deactivate
    ;;
  2)
    echo -e "${YELLOW}Setting up Artist (ManimGL)...${NC}"
    setup_venv "manim-gl-env" ""
    create_demo_scene "scenes/demo_gl.py" "manimgl"
    manimgl scenes/demo_gl.py SimpleDemo -w
    echo -e "${GREEN}Video has been exported to ./media/videos/1080p60/${NC}"
    safe_deactivate
    ;;
  3)
    echo -e "${YELLOW}Setting up Hybrid (CE + OpenGLScene)...${NC}"
    setup_venv "manim-ce-env" "manim"
    create_demo_scene "scenes/demo_ce_opengl.py" "ce"
    manim -pql --renderer=opengl scenes/demo_ce_opengl.py SimpleDemo
    safe_deactivate
    ;;
  4)
    echo -e "${YELLOW}Setting up Lite (CE 2D-only)...${NC}"
    setup_venv "manim-ce-env" "manim"
    create_demo_scene "scenes/demo_simple.py" "ce"
    manim scenes/demo_simple.py SimpleDemo -pql
    safe_deactivate
    ;;
  5)
    echo -e "${YELLOW}Setting up Sharp (CE + MacTeX)...${NC}"
    if ! check_command "latex"; then
        if [[ "$OSTYPE" == "darwin"* ]]; then
            check_command "brew" || {
                echo -e "${RED}Homebrew is required to install MacTeX automatically.${NC}"
                exit 1
            }
            echo -e "${YELLOW}Installing MacTeX (this may take a while)...${NC}"
            brew install --cask mactex-no-gui
        else
            echo -e "${RED}MacTeX auto-install is only supported on macOS with Homebrew.${NC}"
            echo -e "${YELLOW}Please install LaTeX manually if you're on Linux or Windows.${NC}"
            exit 1
        fi
    fi
    setup_venv "manim-ce-env" "manim"
    create_demo_scene "scenes/demo_latex.py" "ce"
    manim scenes/demo_latex.py SimpleDemo -pql
    safe_deactivate
    ;;
  *)
    echo -e "${RED}Invalid choice. Exiting.${NC}"
    exit 1
    ;;
esac
