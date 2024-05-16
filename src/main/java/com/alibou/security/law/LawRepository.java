package com.alibou.security.law;

import com.alibou.security.law.entities.Law;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.UUID;

@Repository
public interface LawRepository extends JpaRepository<Law, UUID> {
}
