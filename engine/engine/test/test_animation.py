import pytest
from engine.engine.animation import TAnimation

def test_animation_init():
    anim = TAnimation()
    assert isinstance(anim, TAnimation)
    assert anim.animations == []

def test_play_animation_stub():
    anim = TAnimation()
    anim.play_animation('move', object())

def test_stop_animation_stub():
    anim = TAnimation()
    anim.stop_animation(1)

def test_update_stub():
    anim = TAnimation()
    anim.update(0.1)

def test_clear():
    anim = TAnimation()
    anim.animations.append('dummy')
    anim.clear()
    assert anim.animations == []

