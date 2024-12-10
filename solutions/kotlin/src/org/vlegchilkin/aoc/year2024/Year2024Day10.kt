package org.vlegchilkin.aoc.year2024

import org.vlegchilkin.aoc.*

const val START: Int = 0
const val FINISH: Int = 9

/**
 * 2024/10: Hoof It
 */
class Year2024Day10(input: String) : Solution {
  private val map = input.toCSpace { it.digitToInt() }

  override fun partA(): Any {
    val routes = map.transform { pos, height -> if (height == START) mutableSetOf(pos) else mutableSetOf() }

    for (height in START + 1..FINISH) {
      map.filterValues { it == height }.keys.forEach { pos ->
        val lowerPositions = map.links(pos, Direction.borders()) { map[it] == height - 1 }
        routes[pos]?.let { posRoutes ->
          lowerPositions.mapNotNull { routes[it] }.forEach { lowerRoutes -> posRoutes.addAll(lowerRoutes) }
        }
      }
    }

    val finishPositions = map.filterValues { it == FINISH }.keys
    val total = finishPositions.mapNotNull { routes[it] }.sumOf { it.size }
    return total
  }

  override fun partB(): Any {
    val pathsCounter = map.transform { _, high -> if (high == START) 1 else 0 }

    for (height in START + 1..FINISH) {
      map.filterValues { it == height }.keys.forEach { pos ->
        val lowerPositions = map.links(pos, Direction.borders()) { map[it] == height - 1 }
        pathsCounter[pos] = lowerPositions.mapNotNull { pathsCounter[it] }.sum()
      }
    }

    val finishPositions = map.filterValues { it == FINISH }.keys
    val total = finishPositions.mapNotNull { pathsCounter[it] }.sum()
    return total
  }

  companion object : Test(2024, 10, { Year2024Day10(it) })
}
