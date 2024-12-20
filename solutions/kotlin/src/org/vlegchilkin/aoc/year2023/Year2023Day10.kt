package org.vlegchilkin.aoc.year2023

import org.vlegchilkin.aoc.*
import org.vlegchilkin.aoc.Direction.*


/**
 * 2023/10: Pipe Maze
 */
class Year2023Day10(input: String) : Solution {
  private val space = input.toCSpace()
  private val start = space.filterValues { it == 'S' }.keys.first()
  private val joints = mapOf(
    '|' to listOf(N, S),
    '-' to listOf(E, W),
    'J' to listOf(W, N),
    'L' to listOf(E, N),
    'F' to listOf(E, S),
    '7' to listOf(W, S)
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
      val step = joints[space[current]]!!.first { (current + it) != prev }
      prev = current
      current += step

      val side = step.turn(Side.R)
      listOf(prev, current).forEach {
        left.add(it - side)
        right.add(it + side)
      }
    }
    val filler = space.expand(1).transform { pos, _ ->
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

    val insideZone = if (filler[-1 to -1] == Zone.L) Zone.R else Zone.L
    val partB = areas[insideZone] ?: 0

    return partA to partB
  }

  companion object : Test(2023, 10, { Year2023Day10(it) })
}
