package org.vlegchilkin.aoc.year2025

import org.vlegchilkin.aoc.*


/**
 * 2025/1: Secret Entrance
 */
class Year2025Day1(input: String) : Solution {
  private val rotations = input.toList { (if (it.first() == 'R') 1 else -1) * it.drop(1).toInt() }
  private val startPosition = 50

  override fun partA(): Any {
    var position = startPosition
    var counter = 0

    for (rotation in rotations) {
      position = (position + rotation).mod(100)
      if (position == 0) counter++
    }

    return counter
  }

  override fun partB(): Any {
    var position = startPosition
    var counter = 0

    for (rotation in rotations) {
      if (rotation > 0) {
        position += rotation
        counter += position / 100
      }
      else {
        if (position == 0) counter -= 1
        position += rotation
        counter += (-position + 100) / 100
      }

      position = position.mod(100)
    }
    return counter
  }

  companion object : Test(2025, 1, { Year2025Day1(it) })
}
