package org.vlegchilkin.aoc.year2020

import org.vlegchilkin.aoc.*
import org.vlegchilkin.aoc.Side.Companion.toSide

class Year2020Day12(input: String) : Solution {
  private val actions = input.toList { it[0] to it.substring(1).toInt() }

  override fun partA(): Int {
    var pos = 0 to 0
    var head = Direction.E
    actions.forEach { (action, steps) ->
      when (action) {
        'F' -> pos += head * steps
        'L', 'R' -> repeat(steps / 90) { head = head.turn(action.toSide()) }
        'N', 'S', 'W', 'E' -> pos += Direction.of(action)!! * steps
      }
    }
    return pos manhattanTo (0 to 0)
  }

  override fun partB(): Int {
    var pos = 0 to 0
    var waypoint = -1 to 10
    actions.forEach { (action, steps) ->
      when (action) {
        'F' -> pos += waypoint * steps
        'L' -> repeat(steps / 90) { waypoint = -waypoint.clockwise() }
        'R' -> repeat(steps / 90) { waypoint = waypoint.clockwise() }
        'N', 'S', 'W', 'E' -> waypoint += Direction.of(action)!! * steps
      }
    }
    return pos manhattanTo (0 to 0)
  }

  companion object : Test(2020, 12, { Year2020Day12(it) })
}