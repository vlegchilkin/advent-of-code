package org.vlegchilkin.aoc.year2024

import org.vlegchilkin.aoc.*
import org.vlegchilkin.aoc.Direction.*


/**
 * 2024/12: Garden Groups
 */
class Year2024Day12(input: String) : Solution {
  private val garden = input.toCSpace(filter = { true })

  enum class Corner(private val side: Direction, private val outer: Direction, private val inner: Direction) {
    TOP_LEFT(N, W, NW), TOP_RIGHT(E, N, NE), BOTTOM_RIGHT(S, E, SE), BOTTOM_LEFT(W, S, SW);

    fun check(pos: C, area: Set<C>) = ((pos + side) !in area) and (((pos + outer) !in area) or ((pos + inner) in area))
  }

  override fun partAB(): Pair<Int, Int> {
    val regionsMap = CSpace<String>(garden.rows, garden.cols, mutableMapOf())
    val idCounter = mutableMapOf<Char, Int>()
    garden.entries.asSequence().filter { (pos) -> pos !in regionsMap }.forEach { (pos, c) ->
      val counter = idCounter.compute(c) { _, counter -> counter?.plus(1) ?: 0 }
      regionsMap[pos] = "$c.$counter"
      regionsMap.fillByTemplate(pos, garden)
    }
    val regionPositions = regionsMap.entries.groupBy({ it.value }, { it.key }).mapValues { it.value.toSet() }

    data class Region(val id: String, val area: Int, val perimeter: Int, val sides: Int)

    val regions = regionPositions.entries.map { (id, positions) ->
      val perimeter = positions.sumOf { pos ->
        Direction.borders().count { (pos + it) !in positions }
      }
      val sides = positions.sumOf { pos ->
        Corner.entries.count { it.check(pos, positions) }
      }
      Region(id, positions.size, perimeter, sides)
    }

    val partA = regions.sumOf { it.area * it.perimeter }
    val partB = regions.sumOf { it.area * it.sides }
    return partA to partB
  }

  companion object : Test(2024, 12, { Year2024Day12(it) })
}
