package org.vlegchilkin.aoc.year2023

import org.vlegchilkin.aoc.*


/**
 * 2023/23: A Long Walk
 */
class Year2023Day23(input: String) : Solution {
  private val space = input.toCSpace { it.takeIf { it != '.' } }
  private val start = 0 to 1
  private val finish = space.rows.last to space.cols.last - 1
  private val directions = Direction.borders()

  override fun partA(): Any {
    var longest = 0

    fun dfs(pos: C, visited: MutableSet<C>) {
      if (pos == finish) {
        longest = longest.coerceAtLeast(visited.size)
        return
      }

      val links = directions.mapNotNull { dir ->
        val nextPos = pos + dir
        val valid = when (val x = space[nextPos]) {
          '#' -> false
          '<', '>', '^', 'v' -> Direction.of(x) == dir
          else -> space.isBelongs(nextPos)
        }
        if (valid && nextPos !in visited) nextPos else null
      }
      for (link in links) {
        visited.add(link)
        dfs(link, visited)
        visited.remove(link)
      }
    }
    dfs(start, mutableSetOf(start))
    return longest - 1
  }

  enum class Type { X, O }

  override fun partB(): Any {
    val graph = mutableMapOf<C, MutableList<Pair<C, Int>>>().apply {
      this[start] = mutableListOf()
      this[finish] = mutableListOf()
    }
    val space = space.transform { pos, c ->
      if (pos in graph) Type.X else if (c != '#') Type.O else null
    }

    fun buildGraph(vertex: C, start: C) {
      var length = 1
      var (prev, pos) = vertex to start
      while (pos !in graph) {
        val links = space.links(pos, directions) { it != prev && it in space }
        if (links.size < 2) {
          space.remove(pos)
          if (links.isEmpty()) return // dead end
          prev = pos
          pos = links.first()
          length += 1
        }
        else {
          space[pos] = Type.X
          graph[pos] = mutableListOf()
          links.forEach {
            buildGraph(pos, it)
          }
        }
      }
      graph[vertex]!!.add(pos to length)
      graph[pos]!!.add(vertex to length)
    }

    buildGraph(start, start + Direction.S)

    fun maxPath(pos: C, visited: Set<C>, length: Int): Int? {
      if (pos == finish) return length
      var best: Int? = null
      for ((next, path) in graph[pos]!!) {
        if (next in visited) continue
        val current = maxPath(next, visited + next, length + path)
        if (current != null && (best == null || best < current)) best = current
      }
      return best
    }


    return maxPath(start, setOf(start), 0)!!
  }

  companion object : Test(2023, 23, { Year2023Day23(it) })
}
