package com.alibou.security.structure;

import com.alibou.security.structure.entity.Structure;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.UUID;
@Repository
public interface StructureRepository extends JpaRepository<Structure, UUID> {
}
