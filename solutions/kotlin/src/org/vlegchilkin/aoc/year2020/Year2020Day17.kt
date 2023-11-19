package org.vlegchilkin.aoc.year2020

import org.vlegchilkin.aoc.*

class Year2020Day17(input: String) : Solution {
  private val area = input.trimSplitMap { it.map { c -> (c == '#') } }

  private fun <T> run(spacer: (Int, Int) -> T, wrapper: (T) -> List<T>): Int {
    var space: Set<T> = area.mapIndexed { x, line ->
      line.mapIndexedNotNull { y, active ->
        if (active) spacer(x, y) else null
      }
    }.flatten().toSet()

    repeat(6) {
      space = space.asSequence().flatMap { pos -> wrapper(pos) }.toSet().filter { pos ->
        val neighbours = wrapper(pos).count { it in space && it != pos }
        neighbours == 3 || neighbours == 2 && pos in space
      }.toSet()
    }
    return space.size
  }

  override fun partA(): Int {
    return run({ x, y -> Triple(x, y, 0) }) { wrap3D(it) }
  }

  override fun partB(): Int {
    return run({ x, y -> listOf(x, y, 0, 0) }) { wrapMultiD(it) }
  }

  companion object : Test(2020, 17, { Year2020Day17(it) })
}