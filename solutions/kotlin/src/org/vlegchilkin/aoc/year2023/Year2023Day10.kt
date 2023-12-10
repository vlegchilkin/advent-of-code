package org.vlegchilkin.aoc.year2023

import org.vlegchilkin.aoc.*


/**
 * 2023/10: Pipe Maze
 */
class Year2023Day10(input: String) : Solution {
  private val space = input.toCSpace { it.takeIf { c -> c != '.' } }
  private val start = space.filterValues { it == 'S' }.keys.first()
  private val joints = mapOf(
    '|' to listOf(Direction.N, Direction.S),
    '-' to listOf(Direction.E, Direction.W),
    'J' to listOf(Direction.W, Direction.N),
    'L' to listOf(Direction.E, Direction.N),
    'F' to listOf(Direction.E, Direction.S),
    '7' to listOf(Direction.W, Direction.S)
  )

  init {
    // resolve correct joint instead of 'S'
    val validJointsPerDirection = joints.flatMap { (k, v) -> v.map { it to k } }.groupBy({ it.first }, { it.second })
    val possibleJoints = joints.filterValues { dirs ->
      dirs.all { space[start + it] in validJointsPerDirection[-it]!! }
    }
    space[start] = possibleJoints.keys.first()
  }

  enum class Zone { F, L, R }


  override fun partAB(): Pair<Int, Int> {
    var prev: C? = null
    var current: C = start
    val fence = mutableSetOf<C>()
    val left = mutableSetOf<C>()
    val right = mutableSetOf<C>()
    while (current !in fence) {
      fence.add(current)
      val move = joints[space[current]]?.firstOrNull { (current + it) != prev }
      val (l, r) = when (move) {
        Direction.N -> Direction.W to Direction.E
        Direction.S -> Direction.E to Direction.W
        Direction.W -> Direction.S to Direction.N
        Direction.E -> Direction.N to Direction.S
        else -> throw IllegalArgumentException()
      }
      prev = current
      current += move
      listOf(prev, current).forEach {
        left.add(it + l)
        right.add(it + r)
      }
    }
    val filler = space.transform { pos, _ ->
      when (pos) {
        in fence -> Zone.F
        in left -> Zone.L
        in right -> Zone.R
        else -> null
      }
    }
    filler.filterValues { it != Zone.F }.forEach { (pos, c) ->
      filler.fill(pos) { c }
    }
    val areas = filler.values.groupingBy { it }.eachCount()
    val partA = (areas[Zone.F] ?: 0) / 2
    val partB = minOf(areas[Zone.L] ?: 0, areas[Zone.R] ?: 0) // any side might be the inside, but there are only two options to guess

    return partA to partB
  }

  companion object : Test(2023, 10, { Year2023Day10(it) })
}
